from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import group_members,UserInfoByIdView,DeleteGroupView,leave_group,join_group,ShopIdView,RegisterView,ShopOwnerListView,LikeStatusView,CommentViewSet,DislikeView,LikeViewSet,ShopDetailView,UserInfoView,ShopOwnerDetailView,CreateShopOwnerView,CustomTokenObtainPairView,DeleteAccountView,UserListView,UpdateUserInfoView
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('register/', RegisterView.as_view(), name='register'),
    path('user-info/<str:username>/', UserInfoView.as_view(), name='user_info'),
    path('user-info/id/<int:user_id>/', UserInfoByIdView.as_view(), name='user_info_by_id'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('user/update/', UpdateUserInfoView.as_view(), name='update-user-info'),
    # path('create-shop-owner/', CreateShopOwnerView.as_view(), name='create_shop_owner'),
    path('shop/create/', CreateShopOwnerView.as_view(), name='create-shop-owner'),
    path('shop/', ShopOwnerDetailView.as_view(), name='shop-owner-detail'),
    
    path('posts/<int:post_id>/like-status/', LikeStatusView.as_view(), name='like-status'),
    path('posts/<int:post_id>/dislike/', DislikeView.as_view(), name='dislike-post'),
    
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('shop_id/', ShopIdView.as_view(), name='shop-id'),
    path('shop/<int:pk>/', ShopDetailView.as_view(), name='shop-detail'),
    path('shops/', ShopOwnerListView.as_view(), name='shop-owner-list'),
    
    
    path('chat/<str:room_name>/', views.room, name='room'),
    
    
    
    
    path('groups/<int:group_id>/join/', join_group, name='join_group'),
    path('groups/<int:group_id>/leave/', leave_group, name='leave_group'),
    path('groups/<int:group_id>/members/', group_members, name='group_members'),
    path('groups/<int:group_id>/delete/', DeleteGroupView.as_view(), name='delete-group'),


    

] 