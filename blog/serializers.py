from django.contrib.auth.models import User
from .models import Blog
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserFullSerializer(serializers.HyperlinkedModelSerializer):
    blogs = serializers.HyperlinkedIdentityField(view_name="blog-detail", many=True, lookup_field='pk')

    class Meta:
        model = User
        fields = ['username', 'email', 'blogs']

class BlogSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="blog-detail", lookup_field='pk')
    created_on = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = Blog
        fields = ['url','id','title','content','author','created_on']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['author'] = UserSerializer(instance.author).data
        return response