import factory
from django.contrib.auth.models import User, Permission

from ads.models import Ads
from contracts.models import Contracts
from customers.models import Customers
from leads.models import Leads
from products.models import Products
from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')

    @factory.post_generation
    def set_permissions(self, create, extracted, **kwargs):
        """
        Метод для назначения прав пользователю после его создания.
        """
        if not create:
            # Объект ещё не сохранен в базе, пропускаем.
            return

        if extracted:
            # Назначаем переданные права, если они указаны.
            self.user_permissions.add(*extracted)


class ManagerUserFactory(UserFactory):
    """
    Фабрика для создания пользователя с менеджерскими правами.
    """
    @factory.post_generation
    def set_permissions(self, create, extracted, **kwargs):
        if not create:
            return

        # Назначаем права менеджера
        permissions = Permission.objects.filter(codename__in=[
            'view_leads',
            'change_leads',
            'view_contracts',
            'add_contracts',
            'change_contracts',
            'view_customers',
            'add_customers',
            'change_customers',
        ])
        self.user_permissions.add(*permissions)


class OperatorUserFactory(UserFactory):
    """
    Фабрика для создания пользователя с правами оператора.
    """
    @factory.post_generation
    def set_permissions(self, create, extracted, **kwargs):
        if not create:
            return

        # Назначаем права оператора
        permissions = Permission.objects.filter(codename__in=[
            'view_leads',
            'change_leads',
            'add_leads',
        ])
        self.user_permissions.add(*permissions)



class MarketingUserFactory(UserFactory):
    """
    Фабрика для создания пользователя с правами маркетолога.
    """
    @factory.post_generation
    def set_permissions(self, create, extracted, **kwargs):
        if not create:
            return

        # Назначаем права маркетолога
        permissions = Permission.objects.filter(codename__in=[
             'view_ads',
            'add_ads',
            'change_ads',
            'view_products',
            'add_products',
            'change_products',
        ])
        self.user_permissions.add(*permissions)


class AdminUserFactory(UserFactory):
    """
    Фабрика для создания администратора.
    """
    is_superuser = True
    is_staff = True

    @factory.post_generation
    def set_permissions(self, create, extracted, **kwargs):
        if not create:
            return

        pass


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Products

    title = factory.Faker('sentence', nb_words=2)
    description = factory.Faker('text', max_nb_chars=200)
    price = factory.Faker('random_int', min=100, max=10000)


class AdsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ads

    title = factory.Faker('sentence', nb_words=2)
    advertised_service = factory.SubFactory(ProductFactory)
    promotion_channel = factory.Faker('word')
    advertising_budget = factory.Faker('random_int', min=1000, max=50000)



class LeadsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Leads

    first_name = factory.Faker('first_name', locale='ru_RU')
    last_name = factory.Faker('last_name', locale='ru_RU')
    # phone_number = factory.Faker('phone_number', locale='ru_RU')
    phone_number = "+7(958)3322521"
    email = factory.Faker('email', locale='ru_RU')
    promotion_channel = factory.SubFactory(AdsFactory)


class ContractFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contracts

    title = factory.Faker('sentence', nb_words=1)
    service_provided = factory.SubFactory(ProductFactory)
    # service_provided = factory.SubFactory(ProductFactory)
    file = factory.django.FileField(filename="contract.pdf")
    start_date = factory.LazyFunction(timezone.now)
    end_date = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=30))
    amount = factory.Faker('random_int', min=500, max=100000)
    manager = factory.SubFactory(UserFactory)


class CustomersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customers

    lead = factory.SubFactory(LeadsFactory)
    contract = factory.SubFactory(ContractFactory)