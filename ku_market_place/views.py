from django.http import Http404
from django.urls import reverse
from django.views import generic, View
from ku_market_place.models import Product, Order, OrderItem, Customer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


class ProductView(generic.ListView):
    template_name = 'ku_market_place/products.html'
    context_object_name = 'product_lists'

    def get_queryset(self):
        """Return products list."""
        return Product.objects.all()

    def get(self, request, *args, **kwargs):
        search_product = request.GET.get('search')
        if search_product:
            product_lists = Product.objects.filter(
                Q(product_name__icontains=search_product)
            )
            if product_lists:
                print("has product_lists")
                return render(
                    request,
                    self.template_name,
                    context={"product_lists": product_lists},
                )
            print("product_lists is empty")

            return render(
                request,
                self.template_name,
                context={"product_lists": []},

            )
        print("1")
        print("search_product is empty")
        print(f"list: {list(self.get_queryset())}")
        return render(
            request,
            self.template_name,
            context={"product_lists": self.get_queryset()},
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


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        return render(request, 'ku_market_place/cart.html')
