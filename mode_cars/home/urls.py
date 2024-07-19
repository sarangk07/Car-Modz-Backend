from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView,UserInfoView,CreateShopOwnerView,CustomTokenObtainPairView,DeleteAccountView,UserListView,UpdateUserInfoView
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
# router.register(r'users', views.UserDataViewSet)
# router.register(r'shopowners', views.ShopOwnerViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'likes', views.LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('register/', RegisterView.as_view(), name='register'),
    path('user-info/<str:username>/', UserInfoView.as_view(), name='user_info'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('user/update/', UpdateUserInfoView.as_view(), name='update-user-info'),
    path('create-shop-owner/', CreateShopOwnerView.as_view(), name='create_shop_owner'),
    
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),

] 