from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product
from authentication.models import User

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', args=[1])
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        self.client.force_authenticate(user=self.admin_user)

    def test_create_product(self):
        data = {'name': 'Test Product', 'price': 100}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Test Product')

    def test_update_product(self):
        product = Product.objects.create(name='Initial Product', price=50)
        data = {'name': 'Updated Product', 'price': 75}
        response = self.client.put(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(id=product.id).name, 'Updated Product')

    def test_delete_product(self):
        product = Product.objects.create(name='To be deleted', price=25)
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=product.id).exists())
