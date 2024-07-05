from rest_framework import serializers
from .models import UserData, ShopOwner, Product, Post, Comment, Like
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserData
        fields = ['username', 'email', 'password', 'fullname', 'car', 'profile_pic', 'is_shopOwner']

    def create(self, validated_data):
        user = UserData.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            fullname=validated_data.get('fullname', ''),
            car=validated_data.get('car', ''),
            profile_pic=validated_data.get('profile_pic', None),
            is_shopOwner=validated_data.get('is_shopOwner', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'fullname', 'is_shopOwner')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print(f"Attempting to authenticate user: {attrs['username']}")
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = UserSerializer(self.user).data
        return data

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id', 'username', 'email', 'fullname', 'car', 'profile_pic', 'is_shopOwner']

class ShopOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOwner
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
