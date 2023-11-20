from django import forms


class CartForm(forms.Form):
    item_id = forms.IntegerField(
        label="Item ID",
        widget=forms.HiddenInput(),
    )
    quantity = forms.IntegerField(
        label="Quantity",
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quantity',
        })
    )