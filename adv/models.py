from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from django.db import models
from PIL import Image
import uuid

# Create your models here.


class Tag(models.Model):
    tag = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.tag


class Cat(models.Model):
    cat = models.CharField(max_length=20)
    logo = models.CharField(max_length=40, null=True)
    id = models.IntegerField(primary_key=True, editable=True, auto_created=True)
    tag = models.ManyToManyField(Tag, through='TagLink')

    def __str__(self):
        return self.cat


class Sub(models.Model):
    sub = models.CharField(max_length=20)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, through='TagLink')

    def __str__(self):
        return self.sub


class TagLink(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, null=True)
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = [['tag', 'sub', 'cat']]


class Ad(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False, null=False)
    title = models.CharField(max_length=70, null=True)
    description = models.CharField(max_length=600, null=True)
    phone_number = models.CharField(max_length=8, null=True)
    price = models.FloatField(max_length=12, null=True)
    url = models.ImageField(max_length=100, default='default.png', null=True, upload_to='')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    count = models.IntegerField(default=0)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, null=True)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, null=True)

    def __uuid__(self):
        return self.id

    def saved(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.url.path)
        if img.height > 400 or img.weight > 700:
            output_size = (700, 400)
            img.thumbnail(output_size)
            img.save(self.url.path)


class Pic(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, default=None, null=True)
    url = models.ImageField(default='default.png', upload_to='', max_length=70)

    def __uuid__(self):
        return self.ad.id

    def saved(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.url.path)
        if img.height > 400 or img.weight > 700:
            output_size = (700, 400)
            img.thumbnail(output_size)
            img.save(self.url.path)

