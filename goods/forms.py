import math
from django import forms
from django.db.models import Min, Max
from .models import Goods, Price, GoodsCategories, Discount


class CreateGoodsForm(forms.ModelForm):
    picture = forms.ImageField(label=u'Изображение',
                               widget=forms.FileInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Goods
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 5, 'class': 'form-input'}),
        }


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = "__all__"


class SetPrice(forms.ModelForm):
    class Meta:
        model = Price
        fields = "__all__"
        exclude = ['date_time_actual', 'good_id']
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
            'date_time_actual': forms.DateTimeInput(attrs={'class': 'form-input'}),
        }


class GoodsCategoriesRadio(forms.ModelForm):
    @staticmethod
    def set(self):
        self.min_price_filter = forms.CharField(max_length=10,
                                                widget=forms.NumberInput(attrs={'class': 'price-filter'}),
                                                initial=44)

    all_categories_objs = GoodsCategories.objects.all()
    min_goods_price = math.floor(Goods.objects.aggregate(Min('current_price'))['current_price__min'])
    max_goods_price = math.ceil(Goods.objects.aggregate(Max('current_price'))['current_price__max'])
    min_price_filter = forms.CharField(max_length=10, widget=forms.NumberInput(attrs={'class': 'price-filter'}),
                                       initial=min_goods_price)
    max_price_filter = forms.CharField(max_length=10, widget=forms.NumberInput(attrs={'class': 'price-filter'}),
                                       initial=max_goods_price)
    all_ids = [elm.id for elm in all_categories_objs]
    selected_categories = forms.ModelMultipleChoiceField(queryset=all_categories_objs, required=False,
                                                         widget=forms.CheckboxSelectMultiple(
                                                             attrs={'class': 'category'}),
                                                         initial=all_ids)

    class Meta:
        model = GoodsCategories
        fields = ["selected_categories",
                  "min_price_filter",
                  "max_price_filter"]
