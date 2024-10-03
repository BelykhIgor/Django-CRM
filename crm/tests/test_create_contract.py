import os

from django.conf import settings
from django.test import TestCase

from contracts.models import Contracts
from tests.factories import UserFactory, ContractFactory


class ContractTestCase(TestCase):

    def setUp(self):
        # Создаем контракты и пользователей с помощью фабрик
        self.manager = UserFactory(username='manager_test')
        self.contract = ContractFactory(manager=self.manager)

    def test_contract_creation(self):
        # Проверяем, что контракт был создан правильно
        self.assertIsNotNone(self.contract.pk)
        self.assertEqual(self.contract.manager.username, 'manager_test')

    def test_contract_amount_range(self):
        # Проверяем, что сумма контракта находится в нужном диапазоне
        self.assertGreaterEqual(self.contract.amount, 500)
        self.assertLessEqual(self.contract.amount, 100000)

    def test_contract_dates(self):
        # Проверяем, что даты контракта корректно заданы
        self.assertLess(self.contract.start_date, self.contract.end_date)

    def test_delete_contract(self):
        self.contract.delete()
        with self.assertRaises(Contracts.DoesNotExist):
            Contracts.objects.get(pk=self.contract.pk)

    def tearDown(self):
        """
        Удаление файлов контракта после выполнения тестов
        """
        if self.contract.file:  # Убедимся, что файл существует
            file_path = os.path.join(settings.MEDIA_ROOT, self.contract.file.name)
            if os.path.exists(file_path):
                os.remove(file_path)
