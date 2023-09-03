from django.contrib import admin
from .models import Goods, GoodsCategories

# Register your models here.
admin.site.register(Goods)
admin.site.register(GoodsCategories)
