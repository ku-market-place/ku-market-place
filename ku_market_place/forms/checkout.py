from django import forms


class CheckOutForm(forms.Form):
    new_shipping_address = forms.CharField(
        label='Shipping Address',
        max_length=255,
        initial='',  # Set the initial value to the customer's address
        required=True
    )
    payment_method = forms.ChoiceField(
        label='Payment Method',
        choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')]
    )