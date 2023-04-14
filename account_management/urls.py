from django.urls import path
from account_management.views import Signup, Signin, VerifyEmail, ReSendOTP

urlpatterns = [
    path('signup/', Signup.as_view(), name="signup"),
    path('resend/otp/', ReSendOTP.as_view(), name='resend_otp'),
    path('verify/email/', VerifyEmail.as_view(), name="verify_email"),
    path('signin/', Signin.as_view(), name="signin"),
]
