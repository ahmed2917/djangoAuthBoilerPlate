from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status

from .serializer import SignupSerializer, EmailVerifySerializer, ResendOTPSerializer, SigninSerializer
from .common import Common_functions
from utils.response import success_response, failed_response

common_function_obj = Common_functions()
User = get_user_model()

class Signup(APIView):

    def post(self, *args, **kwargs):
        serialized_data = SignupSerializer(data=self.request.data)
        if serialized_data.is_valid():
            instance = serialized_data.save()
            if common_function_obj.send_email_verification(serialized_data.data["email"], instance):
                response = success_response(None, "User signedup successfully", None, state=status.HTTP_200_OK)
                return Response(response)
        else:
            response = failed_response(None, serialized_data.errors, None, state=status.HTTP_400_BAD_REQUEST)
            return Response(response)
        
class Signin(APIView):

    def post(self, *args, **kwargs):
        serialized_data = SigninSerializer(data=self.request.data)
        if serialized_data.is_valid():
            user = authenticate(
                username = serialized_data.data.get('username', ''),
                password = serialized_data.data.get('password', ''),
                )
            if user:
                token, _  = Token.objects.get_or_create(user=user)
                data = {
                    "username" : serialized_data.data.get('username'),
                    "token" : str(token)
                } 
                response = success_response(data, "User signedin successfully", None, state=status.HTTP_200_OK)
                return Response(response)
            else:
                response = success_response(None, "Invalid login credentials", None, state=status.HTTP_401_UNAUTHORIZED)
                return Response(response)
        else:
            response = failed_response(None, serialized_data.errors, None, state=status.HTTP_400_BAD_REQUEST)
            return Response(response)
            
class ReSendOTP(APIView):
    
    def post(self, *args, **kwargs):
        serialized_data = ResendOTPSerializer(data=self.request.data)
        if serialized_data.is_valid():
            user = User.objects.filter(email__exact = serialized_data.data["email"]).first()
            if common_function_obj.send_email_verification(serialized_data.data["email"], user):
                response = success_response(None, "OTP sent successfully", None, state=status.HTTP_200_OK)
                return Response(response)
        else:
            response = failed_response(None, serialized_data.errors, None, state=status.HTTP_400_BAD_REQUEST)
            return Response(response)
        
class VerifyEmail(APIView):
    
    def post(self, *args, **kwargs):
        user = User.objects.filter(email__exact=self.request.data.get('email', '')).first()
        serialized_data = EmailVerifySerializer(data=self.request.data)
        if serialized_data.is_valid():
            user.is_active = True
            user.save()
            response = success_response(None, "Email verified successfully", None, state=status.HTTP_200_OK)
            return Response(response)
        else:
            response = failed_response(None, serialized_data.errors, None, state=status.HTTP_400_BAD_REQUEST)
            return Response(response)