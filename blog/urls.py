from django.urls import path,include
from rest_framework import routers
from .views import UserViewSet, UserFullView, BlogListView,BlogDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('userlist/',UserFullView.as_view(),name='user-list'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('blogs/',BlogListView.as_view(),name='blog-list'),
    path('blogs/<int:pk>/',BlogDetailView.as_view(),name="blog-detail")
]
