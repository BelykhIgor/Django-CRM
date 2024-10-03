# import os
#
# from django.contrib.auth.models import User, Permission
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.test import TestCase
# from django.utils import timezone
# from ads.models import Ads
# from contracts.models import Contracts
# from customers.models import Customers
# from leads.models import Leads
# from products.models import Products
#
#
# class CustomersTest(TestCase):
#     """Функциональный тест."""
#     def setUp(self):
#         # Создаем тестовый продукт.
#         self.products = Products.objects.create(
#             title="New product",
#             description="Test product description",
#             price=500,
#         )
#         # Создаем тестовую рекламную компанию.
#         self.ads = Ads.objects.create(
#             title="Test ads title",
#             advertised_service=self.products,
#             promotion_channel="Test chanel promotion",
#             advertising_budget=100,
#         )
#         # Создаем тестового потенциального клиента.
#         self.lead = Leads.objects.create(
#             first_name="Lead First name",
#             last_name="Lead Last Name",
#             phone_number="89268885544",
#             email="info@mail.com",
#             promotion_channel=self.ads,
#         )
#         # Создаем тестовый файл контракта.
#         self.test_file = SimpleUploadedFile(
#             "test_file.txt",
#             b"Test file content",
#             content_type="text/plain"
#         )
#         # Создаем тестового менеджера.
#         self.manager = User.objects.create(
#             username='user',
#             email='user@example.com',
#             password='userpass'
#         )
#         # Даем права тестовому менеджеру.
#         permissions = Permission.objects.filter(codename__in=[
#             'view_leads',
#             'change_leads',
#             'view_customers',
#             'add_customers',
#             'change_customers',
#             'view_contracts',
#             'add_contracts',
#             'change_contracts'
#         ])
#
#         # Применяем права.
#         self.manager.user_permissions.add(*permissions)
#         # Создаем тестовый контракт.
#         self.contract = Contracts.objects.create(
#             title="Test Contract",
#             service_provided=self.products,
#             file=self.test_file,
#             start_date=timezone.now(),
#             end_date=timezone.now(),
#             amount=1000,
#             manager=self.manager,
#         )
#
#     def test_customers_creation(self):
#         # Создаем тестового активного клиента.
#         customers_instance = Customers.objects.create(lead=self.lead, contract=self.contract)
#         # Тестируем данные активного клиента.
#         self.assertEqual(customers_instance.lead.first_name, "Lead First name")
#         self.assertEqual(customers_instance.lead.last_name, "Lead Last Name")
#         self.assertEqual(customers_instance.lead.phone_number, "89268885544")
#         self.assertEqual(customers_instance.lead.email, "info@mail.com")
#         self.assertIsInstance(customers_instance.lead.promotion_channel, Ads)
#
#
#     def test_document_creation(self):
#         # Тестируем создание объекта с файлом
#         self.document = self.contract
#
#         # Проверяем, что объект был создан
#         self.assertIsNotNone(self.document)
#
#         # Проверяем, что загруженный файл соответствует ожидаемому
#         self.assertEqual(self.document.file.name, "uploaded_files/test_file.txt")
#         self.assertTrue(self.document.file.size > 0)
#
#     def tearDown(self):
#         # Удаляем загруженные файлы после теста
#         if os.path.exists(self.document.file.path):
#             os.remove(self.document.file.path)
