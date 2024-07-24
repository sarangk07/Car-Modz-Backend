
from rest_framework import serializers
from .models import UserData, ShopOwner, Product, Post, Comment, Like,Follow
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

# class UserDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserData
#         fields = ('id', 'username', 'email', 'fullname', 'car','profile_pic', 'is_shopOwner')


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ('id', 'username', 'fullname', 'profile_pic')
        

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']       
              
        
class UserDataSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = UserData
        fields = ('id', 'username', 'email', 'fullname', 'car', 'profile_pic', 'is_shopOwner', 'followers', 'following')

    def get_followers(self, obj):
        followers = Follow.objects.filter(followed=obj)
        return FollowSerializer(followers, many=True).data

    def get_following(self, obj):
        following = Follow.objects.filter(follower=obj)
        return FollowSerializer(following, many=True).data


class UserSerializer(serializers.ModelSerializer):
    shop_id = serializers.SerializerMethodField()

    class Meta:
        model = UserData
        fields = ['id', 'username', 'email', 'fullname', 'car', 'profile_pic', 'is_shopOwner', 'shop_id']

    def get_shop_id(self, obj):
        if hasattr(obj, 'shopowner'):
            return obj.shopowner.id
        return None


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
    
    

    
    
class PostSerializer(serializers.ModelSerializer):
    author = UserDataSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'image', 'author', 'author_type', 'created_at')    

class CommentSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'content', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'post', 'user', 'created_at')
    






























class ShopOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOwner
        fields = ['id', 'user', 'shop_name', 'description', 'shop_image', 'shop_bg_img', 'rating', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at', 'user'] 



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


