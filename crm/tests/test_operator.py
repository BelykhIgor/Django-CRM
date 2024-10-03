from django.test import TestCase
from django.urls import reverse

from leads.models import Leads
from tests.factories import OperatorUserFactory, AdsFactory, LeadsFactory


class OperatorTest(TestCase):

    def setUp(self):
        self.operator = OperatorUserFactory()
        self.operator.set_password('testpassword')
        self.operator.save()
        self.ads = AdsFactory(title="test ads")
        self.url_create = reverse('leads:new_leads')
        self.url_update = lambda pk: reverse('leads:edit_leads', args=[pk])
        self.url_delete = lambda pk: reverse('leads:delete_leads', args=[pk])

        logged_in = self.client.login(username=self.operator.username, password='testpassword')
        self.assertTrue(logged_in)

    def test_permissions(self):
        # Проверяем права оператора.
        permissions = self.operator.get_all_permissions()
        self.assertIn('leads.view_leads', permissions)
        self.assertIn('leads.change_leads', permissions)

    def test_operator_access_to_leads_page(self):
        """
        Проверяем доступ оператора к странице просмотра потенциальных клиентов (leads).
        """
        url_list = [reverse('leads:leads_list')]

        for url in url_list:
            response = self.client.get(url)
            if response.status_code == 302:
                print(f"Redirected to: {response.url}")

            # Оператор должен иметь доступ к этой странице (ожидаем статус 200)
            self.assertEqual(response.status_code, 200)

        # Проверка отсутствия доступа к страницам.
        stop_url_list = [
            reverse('contracts:contract_list'),
            reverse('customers:customers_list'),
            reverse('ads:ads_list'),
        ]

        for url in stop_url_list:
            response = self.client.get(url)
            if response.status_code == 302:
                print(f"Redirected to: {response.url}")

            # Оператор должен иметь доступ к этой странице (ожидаем статус 403)
            self.assertEqual(response.status_code, 403)

    def test_create_lead(self):
        """
        Тестируем создание нового lead через POST-запрос.
        """
        # url = reverse('leads:new_leads')
        promotion_chanel = self.ads.pk
        data = {
            'first_name': 'New',
            'last_name': 'Lead',
            'phone_number': '+7(999)1234567',
            'email': 'newlead@example.com',
            'promotion_channel': promotion_chanel,
        }
        response = self.client.post(self.url_create, data)

        # Проверяем редирект после создания
        self.assertEqual(response.status_code, 302)
        # Проверяем, что объект был создан и данные корректны
        new_lead = Leads.objects.last()
        self.assertEqual(new_lead.first_name, 'New')
        self.assertEqual(new_lead.email, 'newlead@example.com')
        self.assertEqual(new_lead.promotion_channel.pk, promotion_chanel)

    def test_change_lead(self):
        test_lead = LeadsFactory()

        new_data = {
            'first_name': 'Updated',
            'last_name': 'Lead',
            'phone_number': '+7(999)7654321',
            'email': 'updatedlead@example.com',
            'promotion_channel': self.ads.pk,
        }

        response = self.client.post(self.url_update(test_lead.pk), new_data)

        # Проверяем редирект после обновления
        self.assertEqual(response.status_code, 302)

        # Обновляем объект из базы данных
        test_lead.refresh_from_db()

        # Проверяем, что объект был обновлен
        self.assertEqual(test_lead.first_name, 'Updated')
        self.assertEqual(test_lead.email, 'updatedlead@example.com')
        self.assertEqual(test_lead.phone_number, '+7(999)7654321')
        self.assertEqual(test_lead.promotion_channel.pk, self.ads.pk)

    def test_delete_lead(self):
        test_lead = LeadsFactory()
        response = self.client.delete(self.url_delete(test_lead.pk))
        # Проверяем, что у оператора нет прав на удаление записи лида.
        self.assertEqual(response.status_code, 403)


