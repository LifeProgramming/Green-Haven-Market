from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.storage import default_storage
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Items(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True)
    price=models.FloatField()
    image=models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold=models.BooleanField(default=False)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.image:
            storage = default_storage
            path = self.image.path
            if storage.exists(path):
                storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
            return self.name

@receiver(pre_save, sender=Items)
def delete_old_image(sender, instance, **kwargs):
    if instance.pk is None: 
        return

    try:
        old_image = Items.objects.get(pk=instance.pk).image
    except Items.DoesNotExist:
        return

    if old_image and old_image != instance.image:
        storage = default_storage
        if storage.exists(old_image.path):
            storage.delete(old_image.path)

pre_save.connect(delete_old_image, sender=Items)
