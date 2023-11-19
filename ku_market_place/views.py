"""Views for ku_market_place app."""
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ku_market_place.forms import CartForm, CheckOutForm
import random
from django.views import generic, View

from ku_market_place.filters import ProductFilter
from ku_market_place.models import Product, Order, OrderItem


class ProductView(generic.ListView):
    """View for products."""

    queryset = Product.objects.all()
    template_name = 'ku_market_place/products.html'
    context_object_name = 'product_lists'

    def __init__(self, **kwargs):
        """Initialize ProductView."""
        super().__init__(**kwargs)
        self.filterset = None

    def get_queryset(self):
        """Return filtered products list."""
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Return context data."""
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context


class ProductDetailView(generic.DetailView):
    """View for single product."""

    model = Product
    template_name = 'ku_market_place/single-product.html'

    def get(self, request, *args, **kwargs):
        """Return single product."""
        try:
            key = kwargs["pk"]
            product = get_object_or_404(Product, pk=key)
            form = CartForm()
        except Http404:
            messages.warning(
                request,
                f"Product ID {key} does not exist.❗️")
            return redirect("ku-market-place:product")

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
        print(request.user.id)
        form = CheckOutForm()
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.filter(customer_id=customer.id).last()
        if order:
            order_items = order.order_item_id.all()
        else:
            order_items = OrderItem.objects.none()
        try:
            form.fields['new_shipping_address'].initial = customer.address
            return render(request, 'ku_market_place/cart.html', {'order_items': order_items, 'form': form})
        except Customer.DoesNotExist:
            return render(request, 'ku_market_place/cart.html', {'order_items': order_items, 'form': form})

    def post(self, request, *args, **kwargs):
        form = CheckOutForm(request.POST)
        if form:
            customer = Customer.objects.get(user=request.user)
            order = Order.objects.filter(customer_id=customer.id).last()
            order.status = random.choice(['Shipping', 'Delivery', 'Complete'])
            order.save()
            order = Order.objects.create(
                customer_id=customer,
            )
            order.save()
            return redirect('ku-market-place:view_cart')
        return redirect('ku-market-place:view_cart')


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        return redirect('ku-market-place:view_cart')

    def post(self, request, *args, **kwargs):
        form = CartForm(request.POST)
        product_id = kwargs.get("product_id")
        quantity = request.POST.get("quantity")
        print(quantity)

        if form:
            print("form is valid")

            # Assuming you have a Product model, get the product instance
            product = Product.objects.get(pk=product_id)
            # Assuming you have a Cart model, add the product to the cart
            # You may want to associate the product with the user and save it to the cart
            order_item = OrderItem.objects.create(
                product=product,
                quantity=quantity,
                total_amount=product.productPrice * int(quantity),
            )
            order_item.save()
            try:
                customer = Customer.objects.get(user=request.user)
                order = Order.objects.filter(customer_id=customer.id).last()
                order.order_item_id.add(order_item)
                order.save()
            except Order.DoesNotExist:
                order = Order.objects.create(
                    customer_id=Customer.objects.get(user=request.user.id),
                    order_item_id=order_item,
                    total_amount=order_item.total_amount,
                )
                order.save()
            print("success")

            # Redirect to a success page or the same page if needed
            return redirect('ku-market-place:view_cart')

        # If the form is not valid, you can re-render the same template with the form
        return redirect('ku-market-place:view_cart')
