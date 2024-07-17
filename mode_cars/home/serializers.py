
from rest_framework import serializers
from .models import UserData, ShopOwner, Product, Post, Comment, Like
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserData
        fields = ['username', 'email', 'password', 'fullname', 'car', 'profile_pic', 'is_shopOwner','is_admin']

    def create(self, validated_data):
        user = UserData.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            fullname=validated_data.get('fullname', ''),
            car=validated_data.get('car', ''),
            profile_pic=validated_data.get('profile_pic', None),
            is_shopOwner=validated_data.get('is_shopOwner', False),
            # is_admin=validated_data.get('is_admin', False),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ('id', 'username', 'email', 'fullname', 'car','profile_pic', 'is_shopOwner')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ('id', 'username', 'email', 'fullname', 'car', 'profile_pic', 'is_shopOwner')


class TokenSerializers(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise ValidationError("No active account found with the given credentials")

        if user.is_blocked:
            raise ValidationError("User is blocked. Contact admin.")

        if not user.is_active:
            raise ValidationError("User is inactive. Contact admin.")

        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserDataSerializer(user).data
        }

        return data
    
    
    

# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ('id', 'title', 'content', 'image', 'author', 'author_type', 'created_at')   
    
    

class PostSerializer(serializers.ModelSerializer):
    author = UserDataSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'image', 'author', 'author_type', 'created_at')    
    
    
    

class ShopOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOwner
        fields = ['id', 'user', 'shop_name', 'description', 'shop_image', 'shop_bg_img', 'rating', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at']









class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
