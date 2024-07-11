# tests/test_orders.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from cart.models import CartItem
from .models import Order, Product

class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.order_list_url = reverse('order-list')
        self.order_detail_url = reverse('order-detail', args=[1])
        self.product = Product.objects.create(name='Test Product', price=100)
        self.shopping_cart = CartItem.objects.create(product=self.product, quantity=2)

    def test_create_order(self):
        data = {'cart_items': [{'product_id': self.product.id, 'quantity': 2}]}
        response = self.client.post(self.order_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.filter(cart_items__product=self.product).exists())

    def test_delete_order(self):
        order = Order.objects.create()
        response = self.client.delete(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=order.id).exists())
