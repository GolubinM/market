from django import forms
from .models import Goods, Price, GoodsCategories


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
    min_price = forms.CharField(max_length=10)
    max_price = forms.CharField(max_length=10)
    all_categories_objs = GoodsCategories.objects.all()
    all_ids = [elm.id for elm in all_categories_objs]
    selected_categories = forms.ModelMultipleChoiceField(queryset=all_categories_objs, required=False,
                                                         widget=forms.CheckboxSelectMultiple(
                                                             attrs={'class': 'category'}),
                                                         initial=all_ids)

    class Meta:
        model = GoodsCategories
        fields = ["selected_categories",
                  "min_price",
                  "max_price"]
