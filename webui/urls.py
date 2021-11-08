from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import ( BlogView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView,
                     RegisterView, LoginView, LogoutView )

urlpatterns = [
    path('',BlogView.as_view(),name='home'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('blog/<int:pk>/', BlogDetailView.as_view(),name='ui-blog-detail'),
    path('new/',BlogCreateView.as_view(),name='ui-blog-create'),
    path('edit/<int:pk>/',BlogUpdateView.as_view(),name='ui-blog-edit'),
    path('delete/<int:pk>/',BlogDeleteView.as_view(),name='ui-blog-delete'),
]

# there is a way to login using inbuilt auth views
# from django.contrib.auth import views as auth_views
# for reference/details go yahan se check krlena : https://github.com/AmirAhrari/django-blog/blob/master/web/urls.py