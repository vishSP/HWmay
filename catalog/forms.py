from django import forms

from catalog.models import Product, Version


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']

        if 'казино' or 'криптовалюта' or 'крипта' or 'биржа' or 'дешево' or 'бесплатно' or 'обман' or 'полиция' or 'радар' in cleaned_data:
            raise forms.ValidationError('Нарушение правил ввода')
        return cleaned_data


class VersionForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

