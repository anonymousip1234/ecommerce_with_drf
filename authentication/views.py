
# class UserCreateView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistrationSerializer




# @api_view(['POST'])
# @psa('social:complete')
# def exchange_token(request, backend):
#     token = request.data.get('access_token')
#     user = request.backend.do_auth(token)
#     if user:
#         return Response({'token': user.get_token()})
#     else:
#         return Response({'error': 'Authentication failed'}, status=400)


# def send_otp(phone_number):
#     otp = random.randint(1000, 9999)
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     message = client.messages.create(
#         body=f'Your OTP is {otp}',
#         from_=settings.TWILIO_PHONE_NUMBER,
#         to=phone_number
#     )
#     return otp


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, LoginSerializer, OTPLoginSerializer
import random
from django.conf import settings

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPLoginView(APIView):
#     def post(self, request):
#         serializer = OTPLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             otp = random.randint(1000, 9999)
#             client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#             message = client.messages.create(
#             body=f'Your OTP is {otp}',
#             from_=settings.TWILIO_PHONE_NUMBER,
#             to=request.phone_number
#             )
#             return otp
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    pass
