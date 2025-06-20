from rest_framework import serializers

from .models import CustomUser, Profile, Organization, Department, OrganizationContacts, Project, ProjectNotes, ProjectReminder
from django.db.models import Sum
from finance_management.models import FinanceRecord


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']


class OrganizationContactsSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = OrganizationContacts
        fields = ['id', 'organization', 'name',
                  'phone_number', 'email', 'position']


class ProjectSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        write_only=True,
        required=False
    )
    organization_name = serializers.CharField(
        source='organization.name', read_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(
        source='organization.id', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'slug', 'organization',
                  'organization_name', 'organization_id']


class OrganizationSerializer(serializers.ModelSerializer):
    contacts = OrganizationContactsSerializer(
        many=True, required=False)
    projects = ProjectSerializer(many=True, read_only=True)
    person_in_charge = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    opening_balance = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, default=0)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'person_in_charge', 'phone_number', 'address',
                  'remarks', 'opening_balance', 'vat_number', 'contacts', 'projects', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_opening_balance(self, value):
        try:
            if value is None or value == '':
                return 0
            return float(value)
        except (TypeError, ValueError):
            return 0

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts', [])
        # Ensure opening_balance has a default value if not provided or invalid
        opening_balance = validated_data.get('opening_balance')
        if opening_balance is None or opening_balance == '':
            validated_data['opening_balance'] = 0
        else:
            try:
                validated_data['opening_balance'] = float(opening_balance)
            except (TypeError, ValueError):
                validated_data['opening_balance'] = 0

        organization = Organization.objects.create(**validated_data)
        for contact_data in contacts_data:
            OrganizationContacts.objects.create(
                organization=organization, **contact_data)
        return organization

    def update(self, instance, validated_data):
        contacts_data = validated_data.pop('contacts', None)

        # Handle opening_balance
        opening_balance = validated_data.get('opening_balance')
        if opening_balance is not None:
            try:
                validated_data['opening_balance'] = float(opening_balance)
            except (TypeError, ValueError):
                validated_data['opening_balance'] = 0

        # Update organization fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle contacts
        if contacts_data is not None:
            # Get existing contacts
            existing_contacts = {
                contact.id: contact for contact in instance.contacts.all()}

            # Process each contact in the request
            for contact_data in contacts_data:
                contact_id = contact_data.get('id')

                if contact_id and contact_id in existing_contacts:
                    # Update existing contact
                    contact = existing_contacts[contact_id]
                    for attr, value in contact_data.items():
                        setattr(contact, attr, value)
                    contact.save()
                    # Remove from existing_contacts dict to track which ones were updated
                    del existing_contacts[contact_id]
                else:
                    # Create new contact
                    OrganizationContacts.objects.create(
                        organization=instance, **contact_data)

        return instance


class OrganizationDetailSerializer(serializers.ModelSerializer):
    total_receivable = serializers.SerializerMethodField()
    total_payable = serializers.SerializerMethodField()
    total_received = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    contacts = OrganizationContactsSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    def get_balance(self, obj):
        from finance_management.serializers import FinanceRecordBalanceSerializer
        # Get all finance records from all projects of this organization
        finance_records = FinanceRecord.objects.filter(
            organization=obj)
        return FinanceRecordBalanceSerializer(finance_records, many=True).data

    def get_total_receivable(self, obj):
        return FinanceRecord.objects.filter(
            organization=obj,
            transaction_type='Receivable'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

    def get_total_payable(self, obj):
        return FinanceRecord.objects.filter(
            organization=obj,
            transaction_type='Payable'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

    def get_total_received(self, obj):
        return FinanceRecord.objects.filter(
            organization=obj,
            transaction_type='Received'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

    def get_total_paid(self, obj):
        return FinanceRecord.objects.filter(
            organization=obj,
            transaction_type='Paid'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

    class Meta:
        model = Organization
        fields = ['id', 'name', 'person_in_charge', 'phone_number', 'address',
                  'remarks', 'opening_balance', 'vat_number',
                  'total_receivable', 'total_payable', 'total_received', 'total_paid', 'balance', 'contacts', 'projects']
        read_only_fields = ['created_at', 'updated_at']


class OrganizationSmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['id', 'name', 'person_in_charge', 'phone_number', 'address',
                  'vat_number', 'opening_balance', 'remarks']


class ProjectNotesSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = ProjectNotes
        fields = ['id', 'project', 'notes']


class ProjectReminderSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = ProjectReminder
        fields = ['id', 'project', 'title',
                  'description', 'type', 'date', 'is_completed']


class ProjectReminderDetailSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = ProjectReminder
        fields = ['id', 'project', 'title',
                  'description', 'type', 'date', 'is_completed']


class ProjectDetailSerializer(serializers.ModelSerializer):
    organization = OrganizationSmallSerializer()
    project_notes = ProjectNotesSerializer(
        source='notes', many=True, read_only=True)
    project_reminders = ProjectReminderSerializer(
        source='reminders', many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'slug', 'organization',
                  'project_notes', 'project_reminders']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password',
                  'phone_number', 'address', 'opening_balance']
        extra_kwargs = {'password': {'write_only': True}}


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'username', 'email', 'phone_number', 'address']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'profile_picture']
