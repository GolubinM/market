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
    current_price = models.DecimalField(max_digits=8, decimal_places=2)
    favorites_statuses = models.ManyToManyField(User, through="FavoritesStatuses", blank=True)
    compare_statuses = models.ManyToManyField(User, through="CompareStatuses", blank=True,
                                              related_name='compare_goods_set')
    ordered = models.ManyToManyField(User, through="Order", blank=True,
                                     related_name='orders_set')

    def __str__(self):
        return self.title


class Price(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date_time_actual = models.DateTimeField(auto_now=True)
    good_id = models.ForeignKey('Goods', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.price} : {self.good_id} : {self.date_time_actual}"


class Order(models.Model):
    client_id = models.ForeignKey(User, on_delete=models.PROTECT)
    good_id = models.ForeignKey('Goods', on_delete=models.PROTECT, default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    count = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.DateTimeField(default=None, null=True, blank=True)

    def line_total(self):
        return self.count * self.price

    def __str__(self):
        return f"корзина {self.pk} клиент:{self.client_id}"


class GoodsCategories(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class FavoritesStatuses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.goods} is favorites of {self.user}"


class CompareStatuses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.goods} checked as ready-to-compare by {self.user}"


class Discount(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    is_active = models.BooleanField(blank=True, null=True, default=False)
    size_in_percent = models.DecimalField(decimal_places=2, max_digits=3)
    for_each_numbers = models.IntegerField(null=True, blank=True)
    min_order_sum = models.IntegerField(null=True, blank=True)
    for_category = models.ForeignKey(GoodsCategories, on_delete=models.CASCADE, blank=True, null=True)
    for_goods = models.ForeignKey(Goods, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
