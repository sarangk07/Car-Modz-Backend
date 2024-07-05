from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView

router = DefaultRouter()
router.register(r'users', views.UserDataViewSet)
router.register(r'shopowners', views.ShopOwnerViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'likes', views.LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('register/', RegisterView.as_view(), name='register'),
]