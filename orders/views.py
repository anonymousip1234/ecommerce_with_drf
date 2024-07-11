from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from django.db import transaction
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from products.models import Product

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAdminOrReadOnly]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def place_order_from_cart_item(self, request):
        user_id = request.data.get('user')
        cart_item_id = request.data.get('cart_item')

        user = get_object_or_404(get_user_model(), id=user_id)
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=user)

        with transaction.atomic():
            order = Order.objects.create(user=user,status='Confirmed')
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            cart_item.delete()
            # self.send_order_confirmation_email(user.email, order.id)
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def send_order_confirmation_email(self, email, order_id):
        send_mail(
            'Order Confirmation',
            f'Your order {order_id} has been successfully placed.',
            'from@example.com',
            [email],
            fail_silently=False,
        )

