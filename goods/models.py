from django.core.validators import MinValueValidator
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


class Price(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date_time_actual = models.DateTimeField(auto_now=True)
    good_id = models.ForeignKey('Goods', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_time_actual} : {self.price}"


class Order(models.Model):
    client_id = models.ForeignKey(User, on_delete=models.PROTECT)
    good_id = models.ManyToManyField('Goods', blank=True)
    price_id = models.ManyToManyField('Price', blank=True)
    count = models.IntegerField(validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    paid = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return self.title


class GoodsCategories(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title
