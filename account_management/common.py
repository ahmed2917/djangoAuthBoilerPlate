from django.core.mail import send_mail
from django.utils import timezone
import string, secrets

class Common_functions():

    # A simple function to generate 5 digit otp that includes asciiletters and digits
    def generate_otp(self):
        alphabets = string.digits + string.ascii_letters
        otp = "".join(secrets.choice(alphabets) for x in range(5))
        return otp
    
    # A simple function to send otp to defined email address that saves it in db
    def send_email_verification(self, email, instance):
        otp = self.generate_otp()
        send_mail(
            "Email verification",
            f"Enter this OTP to verify your email {otp}",
            "djangodev2024@gmail.com",
            [email],
            fail_silently=False
            )
        instance.otp = otp
        instance.expires_in = timezone.now() + timezone.timedelta(minutes=1)
        instance.save()
        return True
        