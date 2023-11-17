from django import forms


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(label='Shipping Address', max_length=100, required=True)
    payment_method = forms.ChoiceField(label='Payment Method', choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])