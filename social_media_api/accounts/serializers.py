from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Use serializers.CharField() without parameters initially
    password = serializers.CharField()
    password2 = serializers.CharField()
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'bio')
    
    def validate(self, attrs):
        # Add validation manually since we removed validators parameter
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Manually validate password
        try:
            validate_password(attrs.get('password'))
        except Exception as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'bio', 'profile_picture')
