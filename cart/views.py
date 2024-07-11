from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404
from products.models import Product

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart = get_object_or_404(Cart, user=self.request.user)
        return self.queryset.filter(cart=cart)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        product = get_object_or_404(Product, id=self.request.data['product'])
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(self.request.data['quantity'])
            cart_item.save()
        else:
            serializer.save(cart=cart, product=product)
    
    def perform_update(self, serializer):
        cart = get_object_or_404(Cart, user=self.request.user)
        serializer.save(cart=cart)

    def perform_destroy(self, instance):
        instance.delete()
