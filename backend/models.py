from django.db import models
from django.http import  JsonResponse
import json
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100 , unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return json.dumps({"name": self.name, "email": self.email, "password": self.password, "created_at": self.created_at, "updated_at": self.updated_at})

class Task(models.Model):
    user = models.CharField(max_length=50)
    name = models.TextField()
    status = models.CharField(max_length=100, default="todo")    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return json.dumps({"user": self.user, "name": self.name, "status": self.status,"created_at": self.created_at, "updated_at": self.updated_at})
