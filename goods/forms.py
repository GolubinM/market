from django import forms
from .models import Goods


class CreateGoodsForm(forms.ModelForm):
    picture = forms.ImageField(label=u'Фотографии',
                               widget=forms.FileInput(attrs={'multiple': 'multiple', 'class': 'form-input'}))

    class Meta:
        model = Goods
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 5, 'class': 'form-input'}),
            'picture': forms.FileInput(attrs={'multiple': 'multiple', 'class': 'form-input'}),
            # 'publish': forms.TextInput(attrs={'class': 'form-input'}),
            # 'created': forms.TextInput(attrs={'class': 'form-input'}),
            # 'updated': forms.TextInput(attrs={'class': 'form-input'}),
            # 'status': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.TextInput(attrs={'class': 'form-input'}),

        }
