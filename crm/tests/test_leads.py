from django.test import TestCase
from django.urls import reverse

from leads.models import Leads
from tests.factories import AdsFactory, ProductFactory, LeadsFactory


class LeadModelTest(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.ads = AdsFactory(advertised_service=self.product)
        self.lead = LeadsFactory(first_name="Test Lead", promotion_channel=self.ads)

    def test_create_lead(self):
        self.assertIsNotNone(self.lead.pk)
        self.assertEqual(self.lead.first_name, "Test Lead")

    def delete_lead(self):
        self.lead.delete()
        with self.assertRaises(Leads.DoesNotExist):
            Leads.objects.get(pk=self.lead.pk)
