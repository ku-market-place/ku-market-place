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
        """Return filtered products list."""
        queryset = Product.objects.all()
        search_product = self.request.GET.get('search')
        gender_filter = self.request.GET.get('gender')
        print('search_product', search_product)
        print('gender ', gender_filter)

        if search_product:
            queryset = queryset.filter(
                Q(productDisplayName__icontains=search_product)
            )

        if gender_filter:
            queryset = queryset.filter(gender=gender_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gender_lists'] = Product.objects.values_list("gender", flat=True).distinct().order_by("gender")
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)



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
