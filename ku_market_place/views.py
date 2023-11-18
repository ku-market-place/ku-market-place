from django.http import Http404
from django.views import generic
from ku_market_place.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q


class ProductView(generic.ListView):
    template_name = 'ku_market_place/products.html'
    context_object_name = 'product_lists'

    def get_queryset(self):
        """Return products list."""
        return Product.objects.all()

    def get(self, request, *args, **kwargs):
        gender = (Product.objects.values_list("gender", flat=True)
                  .distinct().order_by("gender"))
        search_product = request.GET.get('search')
        if search_product:
            product_lists = Product.objects.filter(
                Q(productDisplayName__icontains=search_product)
            )
            if product_lists:
                return render(
                    request,
                    self.template_name,
                    context={
                        "product_lists": product_lists,
                        "gender_lists": gender
                    },
                )

            return render(
                request,
                self.template_name,
                context={
                    "product_lists": [],
                    "gender_lists": gender
                },
            )

        return render(
            request,
            self.template_name,
            context={
                "product_lists": self.get_queryset(),
                "gender_lists": gender
            }
        )


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
