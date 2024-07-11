from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet,CartViewSet
from django.urls import path


router = DefaultRouter()
router.register(r'cart-items', CartItemViewSet, basename='cart-item')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = router.urls

# urlpatterns = [
#     path('cart-item/', CartItemViewSet.as_view(), name='cart-item'),
#     path('cart/', CartViewSet.as_view(), name='cart'),
# ]