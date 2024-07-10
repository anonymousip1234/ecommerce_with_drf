"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from authentication.views import exchange_token,UserCreateView
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet,BulkUploadView,TaskListView
from cart.views import CartItemViewSet,CartTotalView
from orders.views import OrderViewSet



router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',UserCreateView.as_view(),name='user_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/convert-token/', exchange_token, name='convert_token'),
    path('api/bulk-upload/', BulkUploadView.as_view(), name='bulk_upload'),
    path('api/tasks/', TaskListView.as_view(), name='task_list'),
    path('api/cart/total/', CartTotalView.as_view(), name='cart_total'),
    path('api/', include(router.urls)),

]

