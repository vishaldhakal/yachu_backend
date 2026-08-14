from decimal import Decimal
from typing import Any, Dict

from django.db import transaction
from django.shortcuts import get_object_or_404

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
    bill_file=None,
    component_model: "ComponentModel" = None,
    quantity: Any = 0,
    price_per_item: float = 0.0,
    items_data: list = None,
) -> ComponentPurchase:

    purchase = ComponentPurchase.objects.create(
        vendor=vendor,
        purchase_date=purchase_date,
        notes=notes,
        bill_file=bill_file,
        total_price=0.0,
    )

    grand_total = Decimal("0.0")

    if items_data:
        for item_dict in items_data:
            c_model = item_dict.get("component_model")
            qty = Decimal(str(item_dict.get("quantity", 0)))
            price = Decimal(str(item_dict.get("price_per_item", 0.0)))
            subtotal = qty * price

            target_model = (
                c_model
                if isinstance(c_model, ComponentModel)
                else ComponentModel.objects.get(pk=c_model)
            )

            unit = item_dict.get("unit", ComponentPurchaseItem.UnitChoices.PCS)

            ComponentPurchaseItem.objects.create(
                purchase=purchase,
                component_model=target_model,
                quantity=qty,
                unit=unit,
                price_per_item=float(price),
                total_price=float(subtotal),
            )

            grand_total += subtotal

            # Get or create inventory for this component model and increase stock
            inventory, _ = Inventory.objects.get_or_create(
                component_model=target_model,
                defaults={"quantity": Decimal("0")},
            )
            inventory.quantity = (inventory.quantity or Decimal("0")) + qty
            inventory.save()

    purchase.total_price = float(grand_total)
    purchase.save()

    return purchase


@transaction.atomic
def component_purchase_update(
    *,
    purchase: ComponentPurchase,
    vendor: Vendor = None,
    purchase_date=None,
    notes: str = None,
    bill_file=None,
    items_data: list = None,
) -> ComponentPurchase:
    # Map old items & quantities before clearing
    old_items_map = {}
    for old_item in purchase.items.all():
        m_id = old_item.component_model_id
        old_items_map[m_id] = old_items_map.get(m_id, Decimal("0")) + Decimal(str(old_item.quantity))

    # Clear previous items
    purchase.items.all().delete()

    # Update purchase header
    purchase.vendor = vendor
    purchase.purchase_date = purchase_date
    purchase.notes = notes
    if bill_file is not None:
        purchase.bill_file = bill_file

    grand_total = Decimal("0.0")

    if items_data:
        for item_dict in items_data:
            c_model = item_dict.get("component_model")
            qty = Decimal(str(item_dict.get("quantity", 0)))
            price = Decimal(str(item_dict.get("price_per_item", 0.0)))
            subtotal = qty * price

            target_model = (
                c_model
                if isinstance(c_model, ComponentModel)
                else ComponentModel.objects.get(pk=c_model)
            )

            unit = item_dict.get("unit", ComponentPurchaseItem.UnitChoices.PCS)

            ComponentPurchaseItem.objects.create(
                purchase=purchase,
                component_model=target_model,
                quantity=qty,
                unit=unit,
                price_per_item=float(price),
                total_price=float(subtotal),
            )

            grand_total += subtotal

            # Calculate stock delta vs old purchase item
            old_qty = old_items_map.pop(target_model.id, Decimal("0"))
            delta = qty - old_qty

            # Get or create inventory entry if not already present
            inventory, _ = Inventory.objects.get_or_create(
                component_model=target_model,
                defaults={"quantity": Decimal("0")},
            )

            if delta != 0:
                inventory.quantity = max(Decimal("0"), (inventory.quantity or Decimal("0")) + delta)
                inventory.save()

    # Deduct stock for items that were completely removed in the updated purchase
    for removed_model_id, removed_qty in old_items_map.items():
        inv = Inventory.objects.filter(component_model_id=removed_model_id).first()
        if inv:
            inv.quantity = max(Decimal("0"), (inv.quantity or Decimal("0")) - removed_qty)
            inv.save()

    purchase.total_price = float(grand_total)
    purchase.save()

    return purchase


@transaction.atomic
def project_inventory_used_create(
    *,
    project_id: int,
    inventory: Inventory,
    quantity: Any = 0,
) -> ProjectInventoryUsed:
    quantity = Decimal(str(quantity or 0))

    # Deduct quantity from stock inventory
    current_qty = Decimal(str(inventory.quantity or 0))
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


@transaction.atomic
def inventory_import(*, items_data: list) -> dict:
    created_count = 0
    updated_count = 0

    for item in items_data:
        comp_name = item.get("component_name")
        if not comp_name:
            continue

        model_name = item.get("model_name") or comp_name
        vendor_name = item.get("vendor_name")
        specs = item.get("specs", "")
        qty = Decimal(str(item.get("quantity", 0)))

        vendor_obj = None
        if vendor_name:
            vendor_obj, _ = Vendor.objects.get_or_create(name=vendor_name)

        comp_obj, _ = Component.objects.get_or_create(
            name=comp_name,
            defaults={"vendor": vendor_obj},
        )
        if vendor_obj and not comp_obj.vendor:
            comp_obj.vendor = vendor_obj
            comp_obj.save(update_fields=["vendor", "updated_at"])

        model_obj, _ = ComponentModel.objects.get_or_create(
            component=comp_obj,
            name=model_name,
            defaults={"specs": specs},
        )

        inv, is_new = Inventory.objects.get_or_create(
            component_model=model_obj,
            defaults={"quantity": qty},
        )

        if is_new:
            created_count += 1
        else:
            inv.quantity = (inv.quantity or Decimal("0")) + qty
            inv.save(update_fields=["quantity", "updated_at"])
            updated_count += 1

    return {
        "created_count": created_count,
        "updated_count": updated_count,
        "total_processed": len(items_data),
    }


@transaction.atomic
def tool_import(*, items_data: list) -> dict:
    created_count = 0
    updated_count = 0

    for item in items_data:
        name = item.get("name")
        if not name:
            continue
        qty = int(item.get("quantity", 0))

        tool_obj, is_new = ProjectTool.objects.get_or_create(
            name=name,
            defaults={"quantity": qty},
        )

        if is_new:
            created_count += 1
        else:
            tool_obj.quantity = (tool_obj.quantity or 0) + qty
            tool_obj.save(update_fields=["quantity", "updated_at"])
            updated_count += 1


@transaction.atomic
def import_project_inventory_used(
    *, target_project_id: int, source_project_id: int
) -> dict:
    from ..models import Project, ProjectInventoryUsed

    target_project = get_object_or_404(Project, pk=target_project_id)
    source_project = get_object_or_404(Project, pk=source_project_id)

    imported_inventories = 0
    source_inv_items = ProjectInventoryUsed.objects.filter(
        project=source_project
    ).select_related("inventory", "inventory__component_model")
    for item in source_inv_items:
        inv = item.inventory
        qty = Decimal(str(item.quantity or 0))

        # Check main stock availability before deducting
        current_stock = Decimal(str(inv.quantity or 0))
        if current_stock < qty:
            raise ValueError(
                f"Insufficient stock for inventory item '{inv.component_model.name}'. Available: {current_stock}, Requested: {qty}"
            )

        # Deduct from main inventory stock
        inv.quantity = current_stock - qty
        inv.save(update_fields=["quantity", "updated_at"])

        # Add or update target project inventory used
        target_inv_used, created = ProjectInventoryUsed.objects.get_or_create(
            project=target_project,
            inventory=inv,
            defaults={"quantity": qty},
        )
        if not created:
            target_inv_used.quantity = (target_inv_used.quantity or Decimal("0")) + qty
            target_inv_used.save(update_fields=["quantity", "updated_at"])

        imported_inventories += 1

    return {
        "imported_inventory_items_count": imported_inventories,
        "target_project_id": target_project.id,
        "source_project_id": source_project.id,
    }


@transaction.atomic
def import_project_tool_used(*, target_project_id: int, source_project_id: int) -> dict:
    from ..models import Project, ProjectToolUsed

    target_project = get_object_or_404(Project, pk=target_project_id)
    source_project = get_object_or_404(Project, pk=source_project_id)

    imported_tools = 0
    source_tool_items = ProjectToolUsed.objects.filter(
        project=source_project
    ).select_related("tool")
    for t_item in source_tool_items:
        tool = t_item.tool
        t_qty = t_item.quantity or 0

        # Only check and deduct quantity if tool has tracked quantity stock specified
        if tool.quantity is not None and t_qty > 0:
            current_tool_stock = tool.quantity or 0
            if current_tool_stock < t_qty:
                raise ValueError(
                    f"Insufficient stock for tool '{tool.name}'. Available: {current_tool_stock}, Requested: {t_qty}"
                )
            tool.quantity = current_tool_stock - t_qty
            tool.save(update_fields=["quantity", "updated_at"])

        target_tool_used, created = ProjectToolUsed.objects.get_or_create(
            project=target_project,
            tool=tool,
            defaults={"quantity": t_item.quantity},
        )
        if not created and t_item.quantity is not None:
            if target_tool_used.quantity is None:
                target_tool_used.quantity = t_item.quantity
            else:
                target_tool_used.quantity += t_item.quantity
            target_tool_used.save(update_fields=["quantity", "updated_at"])

        imported_tools += 1

    return {
        "imported_tool_items_count": imported_tools,
        "target_project_id": target_project.id,
        "source_project_id": source_project.id,
    }
