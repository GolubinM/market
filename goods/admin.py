from django.contrib import admin
from .models import Goods, GoodsCategories, Order, Price, FavoritesStatuses, CompareStatuses

# Register your models here.
admin.site.register(Goods)
admin.site.register(GoodsCategories)
admin.site.register(Order)
admin.site.register(Price)
admin.site.register(FavoritesStatuses)
admin.site.register(CompareStatuses)
