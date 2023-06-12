from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Chatbot(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Message(models.Model):
    content = models.TextField()
    role = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.role}: {self.content}"
