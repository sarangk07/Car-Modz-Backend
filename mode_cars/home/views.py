
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserData, ShopOwner, Product, Post, Comment, Like
from .serializers import (
    UserDataSerializer, ShopOwnerSerializer, ProductSerializer, PostSerializer,
    CommentSerializer, LikeSerializer, RegisterSerializer, TokenSerializers
)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenSerializers

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserDataViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer

class ShopOwnerViewSet(viewsets.ModelViewSet):
    queryset = ShopOwner.objects.all()
    serializer_class = ShopOwnerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
