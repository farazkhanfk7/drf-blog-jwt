from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .utils import rename


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.CharField(max_length=200, blank=True, default='')
    author = models.ForeignKey(User,related_name='blogs',on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("ui-blog-detail", kwargs={
            'pk': self.pk
        })

    def get_edit_url(self):
        return reverse("ui-blog-edit", kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse("ui-blog-delete", kwargs={
            'pk': self.pk
        })

    def __str__(self):
        return f"{self.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to=rename('profile_pics')) 
    location = models.CharField(max_length=100, blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)  

    def __str__(self):
        return self.user.username