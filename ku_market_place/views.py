from django.http import Http404
from django.views import generic
from ku_market_place.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ku_market_place.filters import ProductFilter


class ProductView(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'ku_market_place/products.html'
    context_object_name = 'product_lists'

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.filterset = None

    def get_queryset(self):
        """Return filtered products list."""
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gender_lists'] = Product.objects.values_list("gender", flat=True).distinct().order_by("gender")
        context['form'] = self.filterset.form
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'ku_market_place/single-product.html'

    def get(self, request, *args, **kwargs):
        try:
            key = kwargs["pk"]
            product = get_object_or_404(Product, pk=key)
        except Http404:
            messages.warning(
                request,
                f"Product ID {key} does not exist.❗️")
            return redirect("ku-market-place:product")

        return render(
            request,
            self.template_name,
            context={"product": product},
        )


def about(request):
    return render(request, 'ku_market_place/about.html')


def contact(request):
    return render(request, 'ku_market_place/contact.html')


def order_list(request):
    return render(request, 'ku_market_place/order_list.html')
