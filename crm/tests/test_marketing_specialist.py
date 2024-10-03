from django.test import TestCase
from django.urls import reverse

from tests.factories import MarketingUserFactory


class MarketingUserTest(TestCase):

    def setUp(self):
        self.marketing_user = MarketingUserFactory()
        self.marketing_user.set_password('testpassword')
        self.marketing_user.save()

    def test_permissions(self):
        # Проверяем права маркетолога.
        permissions = self.marketing_user.get_all_permissions()
        self.assertIn('ads.view_ads', permissions)
        self.assertIn('ads.change_ads', permissions)

    def test_manager_access_to_leads_page(self):
        """
        Проверяем доступ маркетолога к странице просмотра рекламных компаний.
        """
        logged_in = self.client.login(username=self.marketing_user.username, password='testpassword')
        self.assertTrue(logged_in)

        url_list = [reverse('ads:ads_list')]

        for url in url_list:
            response = self.client.get(url)
            if response.status_code == 302:
                print(f"Redirected to: {response.url}")

            # Маркетолог должен иметь доступ к этой странице (ожидаем статус 200)
            self.assertEqual(response.status_code, 200)

        # Проверка отсутствия доступа к страницам.
        stop_url_list = [
            reverse('contracts:contract_list'),
            reverse('customers:customers_list'),
            reverse('leads:leads_list'),
        ]

        for url in stop_url_list:
            response = self.client.get(url)
            if response.status_code == 302:
                print(f"Redirected to: {response.url}")

            # Менеджер должен иметь доступ к этой странице (ожидаем статус 403)
            self.assertEqual(response.status_code, 403)