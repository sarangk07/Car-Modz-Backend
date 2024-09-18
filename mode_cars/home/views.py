
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserData, ShopOwner, Product, Post, Comment, Like,Follow,Group
from .serializers import (
    UserDataSerializer, ShopOwnerSerializer, ProductSerializer, PostSerializer,
    CommentSerializer, LikeSerializer, RegisterSerializer, TokenSerializers,UserSerializer,GroupSerializer
)
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .serializers import SimpleUserSerializer




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
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
 
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the comment.
        return obj.user == request.user or request.user.is_admin



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LikeStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        is_liked = Like.objects.filter(post_id=post_id, user=request.user).exists()
        return Response({'is_liked': is_liked})


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DislikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            like = Like.objects.get(post_id=post_id, user=request.user)
            like.delete()
            return Response({'message': 'Disliked successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({'error': 'Like does not exist'}, status=status.HTTP_400_BAD_REQUEST)
 
 
 
 
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

    
class ShopOwnerListView(generics.ListAPIView):
    queryset = ShopOwner.objects.all()
    serializer_class = ShopOwnerSerializer
    permission_classes = [IsAuthenticated]


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










from django.shortcuts import render
# Chat room view
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
    
    
    
    







class UserDataViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'shopowner'):
            raise PermissionDenied("Only shop owners can create products.")
        serializer.save(owner=self.request.user.shopowner)

    
    
    def perform_update(self, serializer):
        if hasattr(self.request.user, 'shopowner'):
            serializer.save(owner=self.request.user.shopowner)
        else:
            raise PermissionDenied("Only shop owners can edit products.")
        
    def get_queryset(self):
        
        return Product.objects.all()










class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Set the owner to the current user

@api_view(['POST'])
def join_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    
    # Check if the user is already a member
    if user in group.members.all():
        return Response({"error": "User is already a member of this group"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Add the user to the group
    group.members.add(user)
    
    # Serialize the group data to return
    serializer = GroupSerializer(group)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def leave_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    
    # Check if the user is a member
    if user not in group.members.all():
        return Response({"error": "User is not a member of this group"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Remove the user from the group
    group.members.remove(user)
    
    return Response({"message": "Successfully left the group"}, status=status.HTTP_200_OK)



@api_view(['GET'])
def group_members(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
    
    members = group.members.all()
    serializer = SimpleUserSerializer(members, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteGroupView(generics.DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        group = generics.get_object_or_404(Group, pk=self.kwargs['group_id'])
        # Check if the current user is the owner of the group
        if group.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this group.")
        return group
