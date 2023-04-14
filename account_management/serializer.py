from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    expires_in = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'expires_in']
        
    def validate(self, attrs):
        if User.objects.filter(email__exact=attrs.get('email', '')).exists():
            raise serializers.ValidationError("This email already exists")
        
        if User.objects.filter(username__exact=attrs.get('username', '')).exists():
            raise serializers.ValidationError("This username already exists")
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user
    
class SigninSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def validate(self , attrs):
        user = User.objects.filter(username=attrs.get('username', '')).first()
        if not user:
            raise serializers.ValidationError("This user doesnot exists")
        
        if not user.is_active:
            raise serializers.ValidationError("Please verify email first")
        
        return super().validate(attrs)
    
    
class EmailVerifySerializer(serializers.ModelSerializer):
    otp = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    expires_in = serializers.DateTimeField(required=False, read_only=True)
    
    class Meta:
        model = User
        fields = ['otp','email','expires_in']
    
    def validate(self, attrs):
        user = User.objects.filter(email__exact=attrs.get('email', '')).first()
        
        if not user:
            raise serializers.ValidationError("This email doesnot exists")
        
        if user.is_active is True:
            raise serializers.ValidationError("Email already verified")
        
        if (user.expires_in).timestamp() < (timezone.now()).timestamp():
            raise serializers.ValidationError("OTP expired")
        
        if attrs.get('otp', '') != user.otp:
            raise serializers.ValidationError("OTP is incorrect")
        
        return super().validate(attrs)
            
class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate(self , attrs):
        user = User.objects.filter(email__exact=attrs['email']).first()
        
        if not user:
            raise serializers.ValidationError("This email doesnot exists")
        
        if user.is_active is True:
            raise serializers.ValidationError("Email already verified")
        return attrs