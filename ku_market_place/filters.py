import django_filters
from .models import Product
from django import forms


def get_choice(choices):
    choice_values = Product.objects.values_list(choices, flat=True).distinct().order_by(choices)
    choices = [(choice, choice) for choice in choice_values]

    return choices


class ProductFilter(django_filters.FilterSet):
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


    class Meta:
        model = Product
        fields = {
            "productDisplayName": ["icontains"],
        }

