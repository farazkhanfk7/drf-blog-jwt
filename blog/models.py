from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.CharField(max_length=200, blank=True, default='')
    author = models.ForeignKey(User,related_name='blogs',on_delete=models.CASCADE,default=1)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title}"
