from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User



class Command(BaseCommand):
    help = 'Create default groups with specific permissions'

    def handle(self, *args, **kwargs):
        # Группа администраторы.
        admin_group, created = Group.objects.get_or_create(name='Администраторы')
        permissions = Permission.objects.all()
        admin_group.permissions.set(permissions)

        user = User.objects.get(username='admin')
        user.groups.add(admin_group)

        # Группа Маркетологи.
        user_group, created = Group.objects.get_or_create(name='Маркетологи')
        limited_permissions_ads = Permission.objects.filter(codename__in=[
            'view_ads', 'add_ads', 'change_ads', 'view_products', 'add_products', 'change_products'
        ])
        user_group.permissions.set(limited_permissions_ads)

        # Группа менеджеры.
        user_group, created = Group.objects.get_or_create(name='Менеджеры')
        limited_permissions_managers = Permission.objects.filter(codename__in=[
            'view_leads',
            'change_leads',
            'view_customers',
            'add_customers',
            'change_customers',
            'view_contracts',
            'add_contracts',
            'change_contracts',
        ])
        user_group.permissions.set(limited_permissions_managers)

        # Группа операторы.
        user_group, created = Group.objects.get_or_create(name='Операторы')
        limited_permissions_operators = Permission.objects.filter(codename__in=[
            'view_leads', 'add_leads', 'change_leads'
        ])
        user_group.permissions.set(limited_permissions_operators)

        self.stdout.write(self.style.SUCCESS('Группы и права успешно созданы'))