from django import forms


class CartForm(forms.Form):
    item_id = forms.IntegerField(
        label="Item ID",
        widget=forms.HiddenInput(),
    )
    quantity = forms.IntegerField(
        label="Quantity",
        min_value=1,
        max_value=100,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quantity',
            'min': 1,
            'max': 100,
        })
    )