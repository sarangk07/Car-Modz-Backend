
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserData, ShopOwner, Product, Post, Comment, Like,Follow
from .serializers import (
    UserDataSerializer, ShopOwnerSerializer, ProductSerializer, PostSerializer,
    CommentSerializer, LikeSerializer, RegisterSerializer, TokenSerializers,UserSerializer
)
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes



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
        if not user:
            return Response({"error": "User not found"}, status=404)
        
        serializer = UserDataSerializer(user)
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
        serializer = UserDataSerializer(users, many=True)
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
        
        
 
 
 
# class CreateShopOwnerView(generics.CreateAPIView):
#     queryset = ShopOwner.objects.all()
#     serializer_class = ShopOwnerSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         user = request.user
#         if hasattr(user, 'shopowner'):
#             return Response({"error": "Shop profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=user)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




# class CreateShopOwnerView(generics.CreateAPIView):
#     queryset = ShopOwner.objects.all()
#     serializer_class = ShopOwnerSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(user=user)

# class ShopOwnerDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ShopOwner.objects.all()
#     serializer_class = ShopOwnerSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         user = self.request.user
#         if not hasattr(user, 'shopowner'):
#             raise serializers.ValidationError({"error": "Shop profile does not exist."})
#         return user.shopowner

#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user) 
        


class CreateShopOwnerView(generics.CreateAPIView):
    queryset = ShopOwner.objects.all()
    serializer_class = ShopOwnerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'shopowner'):
            return Response({"error": "Shop profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ShopOwnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShopOwner.objects.all()
    serializer_class = ShopOwnerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if not hasattr(user, 'shopowner'):
            raise serializers.ValidationError({"error": "Shop profile does not exist."})
        return user.shopowner

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        
        
class ShopIdView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'shopowner'):
            return Response({"shop_id": user.shopowner.id})
        return Response({"shop_id": None})      
    
class ShopDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            shop = ShopOwner.objects.get(pk=pk)
            serializer = ShopOwnerSerializer(shop)
            return Response(serializer.data)
        except ShopOwner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    
       


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    try:
        user_to_follow = UserData.objects.get(id=user_id)
    except UserData.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user == user_to_follow:
        return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

    follow, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)

    if created:
        return Response({'message': f'You are now following {user_to_follow.username}'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': f'You are already following {user_to_follow.username}'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        user_to_unfollow = UserData.objects.get(id=user_id)
    except UserData.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        follow = Follow.objects.get(follower=request.user, followed=user_to_unfollow)
        follow.delete()
        return Response({'message': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)
    except Follow.DoesNotExist:
        return Response({'error': f'You are not following {user_to_unfollow.username}'}, status=status.HTTP_400_BAD_REQUEST)       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
        



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
