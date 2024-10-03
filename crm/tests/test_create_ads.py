from django.test import TestCase

from ads.forms import CreateAdsForm
from ads.models import Ads
from tests.factories import ProductFactory, AdsFactory


class AdsTest(TestCase):

    def setUp(self):
        self.product = ProductFactory()
        self.ads = AdsFactory(title="test ads")

    def test_create_ads(self):
        self.assertIsNotNone(self.ads.pk)
        self.assertEqual(self.ads.title, "test ads")

    def test_delete_ads(self):
        self.ads.delete()
        with self.assertRaises(Ads.DoesNotExist):
            Ads.objects.get(pk=self.ads.pk)


class AdsFormTest(TestCase):
    def setUp(self):
        self.product1 = ProductFactory(title="first product")
        self.product2 = ProductFactory(title="second product")

    def test_lead_form_valid(self):
        form = CreateAdsForm()
        self.assertIn(self.product1, form.fields['advertised_service'].queryset)
        self.assertIn(self.product2, form.fields['advertised_service'].queryset)

    def test_form_valid_data(self):
        """
        Тест на корректную валидацию данных.
        """
        form_data = {
            'title': 'Test Ad',
            'advertised_service': self.product1.pk,
            'promotion_channel': 'Online',
            'advertising_budget': 500,
        }
        form = CreateAdsForm(data=form_data)
        self.assertTrue(form.is_valid())

        ad = form.save()
        self.assertEqual(ad.title, 'Test Ad')
        self.assertEqual(ad.advertised_service, self.product1)
        self.assertEqual(ad.promotion_channel, 'Online')
        self.assertEqual(ad.advertising_budget, 500)

    def test_form_invalid_data(self):
        """
        Тест с некорректными данными — без выбора продукта.
        """
        form_data = {
            'title': 'Test Ad',
            'advertised_service': '',
            'promotion_channel': 'Online',
            'advertising_budget': 500,
        }
        form = CreateAdsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('advertised_service', form.errors)  # Ошибка в поле выбора продукта

    def test_empty_product(self):
        """
        Проверяем поведение формы, если пользователь не выбрал продукт.
        """
        form_data = {
            'title': 'Test Ad',
            'advertised_service': '',
            'promotion_channel': 'Online',
            'advertising_budget': 1000
        }
        form = CreateAdsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('advertised_service', form.errors)  # Должна быть ошибка валидации


class AdsViewTest(TestCase):
    def setUp(self):
        pass