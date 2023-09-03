from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Goods(models.Model):
    STATUS_CHOICES = (
        ('published', 'Published'),
        ('unpublished', 'Unpublished')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    picture = models.ImageField(upload_to='goods/images')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='published')
    category = models.ForeignKey('GoodsCategories', on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class GoodsCategories(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title
