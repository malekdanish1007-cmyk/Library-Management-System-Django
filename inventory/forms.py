from django import forms
from .models import Item
import re

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'quantity', 'price']

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
            raise forms.ValidationError(
                'Name must contain only letters, numbers, spaces, hyphens or underscores.'
            )
        return name

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty < 0:
            raise forms.ValidationError('Quantity cannot be negative.')
        return qty

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return price