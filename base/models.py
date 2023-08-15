from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class ForumRoom(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    participiants = models.ManyToManyField(User, related_name='participiants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    room = models.ForeignKey(ForumRoom, on_delete=models.CASCADE, null=False)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated']
    
    def __str__(self):
        return str(self.body[0:50])