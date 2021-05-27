from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Todo(models.Model):
    CHOICES = (
        ('TODO', 'TODO'),
        ('INPROGRESS', 'INPROGRESS'),
        ('DONE', 'DONE'),
        ('CANCELED', 'CANCELED')
    )
    text = models.TextField(max_length=200)
    username = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    status = models.CharField(max_length=200, choices=CHOICES)

    