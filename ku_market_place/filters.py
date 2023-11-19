import django_filters
from .models import Product
from django import forms


def get_choice(choices):
    choice_values = Product.objects.values_list(choices, flat=True).distinct().order_by(choices)
    choices = [(choice, choice) for choice in choice_values]
    return choices


class ProductFilter(django_filters.FilterSet):
    productDisplayName = django_filters.CharFilter(
        label='Product Name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    productPrice = django_filters.RangeFilter()
    gender = django_filters.MultipleChoiceFilter(
        choices=get_choice("gender"),
        widget=forms.CheckboxSelectMultiple,
    )
    masterCategory = django_filters.MultipleChoiceFilter(
        choices=get_choice("masterCategory"),
        widget=forms.CheckboxSelectMultiple,
    )
    subCategory = django_filters.MultipleChoiceFilter(
        choices=get_choice("subCategory"),
        widget=forms.CheckboxSelectMultiple,
    )
    articleType = django_filters.MultipleChoiceFilter(
        choices=get_choice("articleType"),
        widget=forms.CheckboxSelectMultiple,
    )
    baseColour = django_filters.MultipleChoiceFilter(
        choices=get_choice("baseColour"),
        widget=forms.CheckboxSelectMultiple,
    )
    season = django_filters.MultipleChoiceFilter(
        choices=get_choice("season"),
        widget=forms.CheckboxSelectMultiple,
    )
    year = django_filters.MultipleChoiceFilter(
        choices=get_choice("year"),
        widget=forms.CheckboxSelectMultiple,
    )
    usage = django_filters.MultipleChoiceFilter(
        choices=get_choice("usage"),
        widget=forms.CheckboxSelectMultiple,
    )

    PRICE_CHOICES = [
        ('', 'Any'),
        ('asc', 'Ascending'),
        ('desc', 'Descending'),
    ]

    order_by_price = django_filters.ChoiceFilter(
        choices=PRICE_CHOICES,
        method='filter_by_price',
        label='Order by Price',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def filter_by_price(self, queryset, name, value):
        if value == 'asc':
            return queryset.order_by('productPrice')
        elif value == 'desc':
            return queryset.order_by('-productPrice')
        return queryset

    class Meta:
        model = Product
        fields = {
            "productDisplayName": ["icontains"],
        }
