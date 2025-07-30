from django.forms import ModelForm

from page.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
