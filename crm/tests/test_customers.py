import os

from django.conf import settings
from django.test import TestCase

from customers.models import Customers
from tests.factories import (
    LeadsFactory,
    UserFactory,
    ContractFactory,
    CustomersFactory
)


class CustomersTest(TestCase):
    def setUp(self):
        self.lead = LeadsFactory(first_name="Lead First name")
        self.manager = UserFactory(username='manager_test')
        self.contract = ContractFactory(manager=self.manager)
        self.customers = CustomersFactory(lead=self.lead, contract=self.contract)

    def test_customers_creation(self):
        self.assertIsNotNone(self.customers.pk)
        self.assertEqual(self.customers.lead.first_name, 'Lead First name')

    def test_customers_delete(self):
        self.customers.delete()
        with self.assertRaises(Customers.DoesNotExist):
            Customers.objects.get(pk=self.customers.pk)

    def tearDown(self):
        """
        Удаление файлов контракта после выполнения тестов
        """
        if self.contract.file:  # Убедимся, что файл существует
            file_path = os.path.join(settings.MEDIA_ROOT, self.contract.file.name)
            if os.path.exists(file_path):
                os.remove(file_path)
