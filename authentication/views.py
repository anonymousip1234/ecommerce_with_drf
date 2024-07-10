from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from social_django.utils import psa
from rest_framework.response import Response
from rest_framework.decorators import api_view
import random
from twilio.rest import Client
from django.conf import settings

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer




@api_view(['POST'])
@psa('social:complete')
def exchange_token(request, backend):
    token = request.data.get('access_token')
    user = request.backend.do_auth(token)
    if user:
        return Response({'token': user.get_token()})
    else:
        return Response({'error': 'Authentication failed'}, status=400)


def send_otp(phone_number):
    otp = random.randint(1000, 9999)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your OTP is {otp}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return otp