from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserSerializer, BlogSerializer, UserFullSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]

@permission_classes((permissions.IsAuthenticated,))
class UserFullView(APIView):
    """
    List of all Users
    """
    def get_queryset(self,request):
        queryset = User.objects.all()
        return queryset

    def get(self,request,format=None):
        queryset = self.get_queryset(request)
        serializer = UserFullSerializer(queryset, many=True,context={'request': request})
        return Response(serializer.data)


@permission_classes((permissions.IsAuthenticated,))
class BlogListView(APIView):
    """
    List of all Blogs
    """
    def get_queryset(self,request):
        queryset = Blog.objects.all().order_by('-created_on')
        return queryset

    def get(self,request,format=None):
        queryset = self.get_queryset(request)
        serializer = BlogSerializer(queryset, many=True,context={'request': request})
        return Response(serializer.data)


@permission_classes((permissions.IsAuthenticated,)) # This decorator to be used with APIView
class BlogDetailView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk, request):
        try:
            obj = Blog.objects.get(pk=pk)
            return obj
        except Blog.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk, request)
        serializer = BlogSerializer(snippet, context={'request': request})
        return Response(serializer.data)
