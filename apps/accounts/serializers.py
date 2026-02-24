from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
            'username': {'read_only': True},
        }
    
    def create(self, validated_data):
        # Auto-generate username from email (use part before @)
        email = validated_data['email']
        username = email.split('@')[0]
        
        # Use create_user to properly hash the password
        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            name=validated_data['name']
        )
        return user
