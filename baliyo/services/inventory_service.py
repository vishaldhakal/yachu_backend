from typing import Any, Dict

from django.db import transaction

from ..models import (
    BillOfMaterial,
    Component,
    ComponentModel,
    ComponentPurchase,
    ComponentPurchaseItem,
    Inventory,
    ProjectDailyUpdate,
    ProjectInventoryUsed,
    ProjectTool,
    ProjectToolUsed,
    Vendor,
)


def vendor_create(*, name: str, phone_no: str, vendor_address: str = None) -> Vendor:
    return Vendor.objects.create(
        name=name,
        phone_no=phone_no,
        vendor_address=vendor_address,
    )


def vendor_update(*, vendor: Vendor, data: Dict[str, Any]) -> Vendor:
    for field, value in data.items():
        setattr(vendor, field, value)
    vendor.save()
    return vendor


def bill_of_material_create(*, file, vendor: Vendor = None) -> BillOfMaterial:
    return BillOfMaterial.objects.create(file=file, vendor=vendor)


def project_tool_create(*, name: str, quantity: int = None) -> ProjectTool:
    return ProjectTool.objects.create(name=name, quantity=quantity)


@transaction.atomic
def project_tool_used_create(
    *,
    project_id: int,
    tool: ProjectTool,
    quantity: int = None,
) -> ProjectToolUsed:
    if tool.quantity is not None:
        used_qty = quantity if quantity is not None else 1
        current_qty = tool.quantity or 0
        if current_qty < used_qty:
            raise ValueError(
                f"Insufficient quantity for tool {tool.name}. Available: {current_qty}, Requested: {used_qty}"
            )
        tool.quantity = current_qty - used_qty
        tool.save(update_fields=["quantity", "updated_at"])

    obj, created = ProjectToolUsed.objects.get_or_create(
        project_id=project_id,
        tool=tool,
        defaults={"quantity": quantity},
    )
    if not created and quantity is not None:
        obj.quantity = quantity
        obj.save(update_fields=["quantity"])
    return obj


@transaction.atomic
def project_tool_used_update(
    *,
    instance: ProjectToolUsed,
    new_quantity: int = None,
) -> ProjectToolUsed:
    tool = instance.tool
    old_qty = instance.quantity or 0
    target_qty = new_quantity if new_quantity is not None else 0

    if tool.quantity is not None:
        diff = target_qty - old_qty
        if diff > 0:
            if tool.quantity < diff:
                raise ValueError(
                    f"Insufficient quantity for tool {tool.name}. Available: {tool.quantity}, Needed additional: {diff}"
                )
            tool.quantity -= diff
        elif diff < 0:
            tool.quantity += abs(diff)
        tool.save(update_fields=["quantity", "updated_at"])

    instance.quantity = new_quantity
    instance.save(update_fields=["quantity", "updated_at"])
    return instance


@transaction.atomic
def project_tool_used_delete(*, instance: ProjectToolUsed) -> None:
    tool = instance.tool
    used_qty = instance.quantity or 0
    if tool.quantity is not None and used_qty > 0:
        tool.quantity += used_qty
        tool.save(update_fields=["quantity", "updated_at"])
    instance.delete()


def component_create(*, name: str, vendor: Vendor = None) -> Component:
    return Component.objects.create(name=name, vendor=vendor)


def component_model_create(
    *, component: Component, name: str, specs: str = None
) -> ComponentModel:
    return ComponentModel.objects.create(
        component=component,
        name=name,
        specs=specs,
    )


@transaction.atomic
def component_purchase_create(
    *,
    vendor: Vendor = None,
    purchase_date=None,
    notes: str = None,
    component_model: "ComponentModel" = None,
    quantity: int = 0,
    price_per_item: float = 0.0,
    items_data: list = None,
) -> ComponentPurchase:

    purchase = ComponentPurchase.objects.create(
        vendor=vendor,
        purchase_date=purchase_date,
        notes=notes,
        total_price=0.0,
    )

    grand_total = 0.0

    if items_data:
        for item_dict in items_data:
            c_model = item_dict.get("component_model")
            qty = int(item_dict.get("quantity", 0))
            price = float(item_dict.get("price_per_item", 0.0))
            subtotal = qty * price

            target_model = (
                c_model
                if isinstance(c_model, ComponentModel)
                else ComponentModel.objects.get(pk=c_model)
            )

            ComponentPurchaseItem.objects.create(
                purchase=purchase,
                component_model=target_model,
                quantity=qty,
                price_per_item=price,
                total_price=subtotal,
            )

            grand_total += subtotal

            # Get or create inventory for this component model and increase stock
            inventory, _ = Inventory.objects.get_or_create(
                component_model=target_model,
                defaults={"quantity": 0},
            )
            inventory.quantity = (inventory.quantity or 0) + qty
            inventory.save()

    purchase.total_price = grand_total
    purchase.save()

    return purchase


@transaction.atomic
def component_purchase_update(
    *,
    purchase: ComponentPurchase,
    vendor: Vendor = None,
    purchase_date=None,
    notes: str = None,
    items_data: list = None,
) -> ComponentPurchase:
    # Map old items & quantities before clearing
    old_items_map = {}
    for old_item in purchase.items.all():
        m_id = old_item.component_model_id
        old_items_map[m_id] = old_items_map.get(m_id, 0) + old_item.quantity

    # Clear previous items
    purchase.items.all().delete()

    # Update purchase header
    purchase.vendor = vendor
    purchase.purchase_date = purchase_date
    purchase.notes = notes

    grand_total = 0.0

    if items_data:
        for item_dict in items_data:
            c_model = item_dict.get("component_model")
            qty = int(item_dict.get("quantity", 0))
            price = float(item_dict.get("price_per_item", 0.0))
            subtotal = qty * price

            target_model = (
                c_model
                if isinstance(c_model, ComponentModel)
                else ComponentModel.objects.get(pk=c_model)
            )

            ComponentPurchaseItem.objects.create(
                purchase=purchase,
                component_model=target_model,
                quantity=qty,
                price_per_item=price,
                total_price=subtotal,
            )

            grand_total += subtotal

            # Calculate stock delta vs old purchase item
            old_qty = old_items_map.pop(target_model.id, 0)
            delta = qty - old_qty

            # Get or create inventory entry if not already present
            inventory, _ = Inventory.objects.get_or_create(
                component_model=target_model,
                defaults={"quantity": 0},
            )

            if delta != 0:
                inventory.quantity = max(0, (inventory.quantity or 0) + delta)
                inventory.save()

    # Deduct stock for items that were completely removed in the updated purchase
    for removed_model_id, removed_qty in old_items_map.items():
        inv = Inventory.objects.filter(component_model_id=removed_model_id).first()
        if inv:
            inv.quantity = max(0, (inv.quantity or 0) - removed_qty)
            inv.save()

    purchase.total_price = grand_total
    purchase.save()

    return purchase


@transaction.atomic
def project_inventory_used_create(
    *,
    project_id: int,
    inventory: Inventory,
    quantity: int = 0,
) -> ProjectInventoryUsed:
    quantity = quantity or 0

    # Deduct quantity from stock inventory
    current_qty = inventory.quantity or 0
    if current_qty < quantity:
        raise ValueError(
            f"Insufficient stock for {inventory.component_model.name}. Available: {current_qty}, Requested: {quantity}"
        )

    inventory.quantity = current_qty - quantity
    inventory.save()

    return ProjectInventoryUsed.objects.create(
        project_id=project_id,
        inventory=inventory,
        quantity=quantity,
    )


def project_daily_update_create(
    *,
    project_id: int,
    task: str,
    decision: str = None,
    reason: str = None,
    problem: str = None,
) -> ProjectDailyUpdate:
    return ProjectDailyUpdate.objects.create(
        project_id=project_id,
        task=task,
        decision=decision,
        reason=reason,
        problem=problem,
    )
