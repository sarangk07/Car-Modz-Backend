
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserData, ShopOwner, Product, Post, Comment, Like
from .serializers import (
    UserDataSerializer, ShopOwnerSerializer, ProductSerializer, PostSerializer,
    CommentSerializer, LikeSerializer, RegisterSerializer, TokenSerializers,UserSerializer
)
from django.contrib.auth import get_user_model



#login
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenSerializers




#register
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


#loged-in userdata
User = get_user_model()
class UserInfoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        if request.user.username != username:
            return Response({"error": "You can only access your own information"}, status=403)
        
        user = User.objects.filter(username=username).first()
        print("user::::::",User )
        if not user:
            return Response({"error": "User not found"}, status=404)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)


#delete account
class DeleteAccountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "User account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


#all user details
class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#update-profile
class UpdateUserInfoView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserData.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user



#post view/create
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
        
 
 
 
class CreateShopOwnerView(generics.CreateAPIView):
    queryset = ShopOwner.objects.all()
    serializer_class = ShopOwnerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)      
        
        
        
        
        



class UserDataViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
