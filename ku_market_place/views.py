from django.http import Http404
from django.views import generic, View
from ku_market_place.models import Product, Order, OrderItem
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ku_market_place.filters import ProductFilter
from ku_market_place.forms import CartForm
import csv

class ProductView(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'ku_market_place/products.html'
    context_object_name = 'product_lists'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

        image = ""
        with open('ku_market_place/data/images.csv', 'r') as image_csv:
            csv_reader = csv.DictReader(image_csv)
            for row in csv_reader:
                file = row['filename'].replace('.jpg', '')
                if file == str(key):
                    image = row['link']
                    break

        return render(
            request,
            self.template_name,
            context={
                "product": product,
            },
        )


def about(request):
    return render(request, 'ku_market_place/about.html')


def contact(request):
    return render(request, 'ku_market_place/contact.html')


def order_list(request):
    return render(request, 'ku_market_place/order_list.html')


class CartDailView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(customer_id=request.user.id)
        if order:
            # Get all order items related to the order
            order_items = OrderItem.objects.filter(order_item_id=order.id)
        else:
            # If there's no order, set order_items to an empty queryset or handle it accordingly
            order_items = OrderItem.objects.none()
        return render(request, 'ku_market_place/cart.html', {'order_items': order_items})

    def post(self, request, *args, **kwargs):
        form = CartForm(request.POST)

        if form.is_valid():
            # Assuming you have a function to process the form data and create/update the order
            # You might need to adjust this based on your actual model relationships and requirements
            print("form is valid")

            return render(request, 'ku_market_place/order_list.html')  # Redirect to the order list or another page
        else:
            # If the form is not valid, re-render the cart page with the validation errors
            return render(request, 'ku_market_place/cart.html', {'form': form})


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        return render(request, 'ku_market_place/cart.html')
