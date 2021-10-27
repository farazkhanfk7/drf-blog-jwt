from django.urls import path,include
from rest_framework import routers
from .views import UserViewSet, UserFullView, BlogListView,BlogDetailView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('userlist/',UserFullView.as_view(),name='user-list'),
    path('blogs/',BlogListView.as_view(),name='blog-list'),
    path('blogs/<int:pk>/',BlogDetailView.as_view(),name="blog-detail")
]