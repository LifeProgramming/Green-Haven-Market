from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Items(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True)
    price=models.FloatField()
    image=models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold=models.BooleanField(default=False)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name