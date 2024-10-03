import os

from django.contrib.auth.models import Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from contracts.models import Contracts
from products.models import Products


class UploadFileTest(TestCase):
    def setUp(self):
        # Создаем тестовый файл контракта.
        self.test_file = SimpleUploadedFile(
            "test_file.txt",
            b"Test file content",
            content_type="text/plain"
        )
        self.products = Products.objects.create(
            title="New product",
            description="Test product description",
            price=500,
        )
        self.manager = User.objects.create(
            username='user',
            email='user@example.com',
            password='userpass'
        )
        # Даем права тестовому менеджеру.
        permissions = Permission.objects.filter(codename__in=[
            'view_leads',
            'change_leads',
            'view_customers',
            'add_customers',
            'change_customers',
            'view_contracts',
            'add_contracts',
            'change_contracts'
        ])

        # Применяем права.
        self.manager.user_permissions.add(*permissions)
        self.contract = Contracts.objects.create(
            title="Test Contract",
            service_provided=self.products,
            file=self.test_file,
            start_date=timezone.now(),
            end_date=timezone.now(),
            amount=1000,
            manager=self.manager,
        )

    def test_document_creation(self):
        # Тестируем создание объекта с файлом
        self.document = self.contract

        # Проверяем, что объект был создан
        self.assertIsNotNone(self.document)

        # Проверяем, что загруженный файл соответствует ожидаемому
        self.assertEqual(self.document.file.name, "uploaded_files/test_file.txt")
        self.assertTrue(self.document.file.size > 0)

    def tearDown(self):
        # Удаляем загруженные файлы после теста
        if os.path.exists(self.document.file.path):
            os.remove(self.document.file.path)