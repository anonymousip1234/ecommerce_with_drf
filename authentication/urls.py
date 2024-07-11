from django.urls import path
from .views import RegisterView, LoginView, OTPLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('otp-login/', OTPLoginView.as_view(), name='otp-login'),
]
