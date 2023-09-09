from django import forms
from .models import Goods, Price


class CreateGoodsForm(forms.ModelForm):
    picture = forms.ImageField(label=u'Изображение',
                               widget=forms.FileInput(attrs={'class': 'form-input'}))

    # def save(self, commit=True):
        # print(self.fields['current_price'].__str__())
        # print(self.data.get('current_price'))
        # print(*self.data.items())
        # new_price = Price(price=self.data.get('current_price'), good_id=pk)
        # new_price.save()

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
