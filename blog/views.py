from django.shortcuts import render
from django.http import HttpResponse
from .serializers import RegisterSerializer
from rest_framework import generics
from .models import Blog
from django.http import Http404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
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


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
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

    def post(self,request,*args,**kwargs):
        serializer = BlogSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.IsAuthenticatedOrReadOnly,)) # This decorator to be used with APIView
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

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk, request)
        if snippet.author == request.user or request.user.is_superuser:
            serializer = BlogSerializer(snippet, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Unauthorised",status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk, request)
        if snippet.author == request.user or request.user.is_superuser:
            try:
                snippet.delete()
                return Response(data="object deleted successfully", status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response("Unauthorised",status=status.HTTP_403_FORBIDDEN)

        
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
