import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from contracts.models import Contracts
from tests.factories import ManagerUserFactory, ContractFactory, LeadsFactory, ProductFactory
import factory
from django.utils import timezone


class ManagerTest(TestCase):

    def setUp(self):
        self.manager = ManagerUserFactory()
        self.manager.set_password('testpassword')
        self.manager.save()

        self.lead1 = LeadsFactory()
        self.lead2 = LeadsFactory()
        self.product = ProductFactory()
        self.url_create_contract = reverse('contracts:create_contract')
        self.url_update_contract = lambda pk: reverse('contracts:contract_edit', args=[pk])
        logged_in = self.client.login(username=self.manager.username, password='testpassword')
        self.assertTrue(logged_in)


    def test_permissions(self):
        # Проверяем права менеджера.
        permissions = self.manager.get_all_permissions()
        self.assertIn('leads.view_leads', permissions)
        self.assertIn('leads.change_leads', permissions)
        self.assertIn('customers.view_customers', permissions)
        self.assertIn('customers.add_customers', permissions)
        self.assertIn('customers.change_customers', permissions)
        self.assertIn('contracts.view_contracts', permissions)
        self.assertIn('contracts.add_contracts', permissions)
        self.assertIn('contracts.change_contracts', permissions)


    def test_manager_access_to_leads_page(self):
        """
        Проверяем доступ менеджера к странице просмотра страниц.
        """
        logged_in = self.client.login(username=self.manager.username, password='testpassword')
        self.assertTrue(logged_in)

        url_list = [
            reverse('leads:leads_list'),
            reverse('contracts:contract_list'),
            reverse('customers:customers_list'),
        ]

        for url in url_list:
            response = self.client.get(url)
            if response.status_code == 302:
                print(f"Redirected to: {response.url}")

            # Менеджер должен иметь доступ к этой странице (ожидаем статус 200)
            self.assertEqual(response.status_code, 200)
        # Проверка отсутствия доступа к страницам.
        stop_url_list = [
            reverse('ads:ads_list'),
        ]

        # Проверка отсутствия доступа к страницам.
        for url in stop_url_list:
            response = self.client.get(url)
            if response.status_code == 302:
                print(f"Redirected to: {response.url}")

            # Менеджер должен иметь доступ к этой странице (ожидаем статус 403)
            self.assertEqual(response.status_code, 403)

    def test_create_contract(self):
        file = SimpleUploadedFile("contract.pdf", b"file_content", content_type="application/pdf")
        data = {
            "title": "test contract",
            "service_provided": self.product.pk,
            "file": file,
            "start_date": timezone.now().date(),
            "end_date": (timezone.now() + timezone.timedelta(days=30)).date(),
            "amount": 500,
            "manager": self.manager.pk,
        }
        response = self.client.post(self.url_create_contract, data)
        if response.status_code == 302:
            print(f"Redirected to: {response.url}")

        # Проверяем редирект после создания контракта.
        self.assertEqual(response.status_code, 302)
        new_contract = Contracts.objects.last()
        self.assertEqual(new_contract.title, "test contract")
        # Проверка файла контракта.
        self.assertTrue(new_contract.file.name)
        file_path = os.path.join(settings.MEDIA_ROOT, new_contract.file.name)
        self.assertTrue(os.path.exists(file_path))

        if os.path.exists(file_path):
            os.remove(file_path)

    def test_update_contract(self):
        self.contract = ContractFactory()
        file = SimpleUploadedFile("contract_test.pdf", b"file_content", content_type="application/pdf")
        new_contract_data = {
            "title": "update contract",
            "service_provided": self.product.pk,
            "file": file,
            "start_date": timezone.now().date(),
            "end_date": (timezone.now() + timezone.timedelta(days=30)).date(),
            "amount": 500,
            "manager": self.manager.pk,
        }
        response = self.client.post(self.url_update_contract(self.contract.pk), new_contract_data)
        if response.status_code == 302:
            print(f"Redirected after update: {response.url}")
        self.contract.refresh_from_db()
        update_contract = Contracts.objects.last()
        self.assertEqual(update_contract.amount, 500)
        self.assertEqual(update_contract.service_provided, self.product)
        # self.assertEqual(update_contract.manager, self.manager)
        # Проверяем, что название контракта не изменено.
        self.assertNotEqual(update_contract.title, "update contract")

    def test_delete_contract(self):
        pass


    def tearDown(self):
        """
        Удаление файлов контракта после выполнения тестов, если файл существует.
        """
        if hasattr(self, 'contract') and self.contract.file:
            file_path = os.path.join(settings.MEDIA_ROOT, self.contract.file.name)
            if os.path.exists(file_path):
                os.remove(file_path)

        new_contract = Contracts.objects.last()
        if new_contract and new_contract.file:
            file_path = os.path.join(settings.MEDIA_ROOT, new_contract.file.name)
            if os.path.exists(file_path):
                os.remove(file_path)