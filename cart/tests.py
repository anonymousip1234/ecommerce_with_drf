from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CartItem, Product

class ShoppingCartTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cart_url = reverse('cart')
        self.product = Product.objects.create(name='Test Product', price=100)

    def test_add_to_cart(self):
        data = {'product_id': self.product.id, 'quantity': 2}
        response = self.client.post(self.cart_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CartItem.objects.filter(product=self.product).exists())

    def test_remove_from_cart(self):
        cart_item = CartItem.objects.create(product=self.product, quantity=1)
        cart_item_url = reverse('cart', args=[cart_item.id])
        response = self.client.delete(cart_item_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())
