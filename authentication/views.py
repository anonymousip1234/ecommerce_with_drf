


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, LoginSerializer, OTPLoginSerializer
import random
from rest_framework_simplejwt.tokens import RefreshToken
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
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
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
