import django_filters
from .models import Goods


class GoodsPriceFilter(django_filters.FilterSet):
    current_price = django_filters.AllValuesFilter()

    class Meta:
        model = Goods
        fields = {'current_price': ['gt', 'lt']}
