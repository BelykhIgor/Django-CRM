from django.test import TestCase

from products.models import Products
from tests.factories import ProductFactory


class ProductTest(TestCase):
    def setUp(self):
        self.product = ProductFactory(title="test product")

    def test_create_product(self):
        self.assertIsNotNone(self.product.pk)
        self.assertEqual(self.product.title, "test product")

    def test_delete_product(self):
        self.product.delete()
        with self.assertRaises(Products.DoesNotExist):
            Products.objects.get(pk=self.product.pk)