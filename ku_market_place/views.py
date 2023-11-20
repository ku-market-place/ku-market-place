"""Views for ku_market_place app."""
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ku_market_place.forms import CartForm, CheckOutForm
import random
from django.views import generic, View

from ku_market_place.filters import ProductFilter
from ku_market_place.models import Product, Order, OrderItem, Customer


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
                "form": form,
            },
        )


def about(request):
    return render(request, 'ku_market_place/about.html')


def contact(request):
    return render(request, 'ku_market_place/contact.html')


def order_list(request):
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.filter(customer_id=customer.id)
    if orders:
        return render(request, 'ku_market_place/order_list.html', {'orders': orders})
    return render(request, 'ku_market_place/order_list.html')


class CartDailView(View):
    def get(self, request, *args, **kwargs):
        form = CheckOutForm()
        form_delete = CartForm()
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(
                user=request.user,
            )
        order = Order.objects.filter(customer_id=customer.id).last()
        if order:
            order_items = order.order_item_id.all()
            total_amount = order.total_amount
        else:
            order_items = OrderItem.objects.none()
            total_amount = 0
        try:
            form.fields['new_shipping_address'].initial = customer.address
            return render(request, 'ku_market_place/cart.html',
                          {'order_items': order_items, 'form': form,
                           'total_amount': total_amount, 'form_delete': form_delete})
        except Customer.DoesNotExist:
            return render(request, 'ku_market_place/cart.html',
                          {'order_items': order_items, 'form': form,
                           'total_amount': total_amount, 'form_delete': form_delete})

    def post(self, request, *args, **kwargs):
        form = CheckOutForm(request.POST)
        payment = request.POST.get("payment_method")
        if form:
            customer = Customer.objects.get(user=request.user)
            customer.address = request.POST.get("new_shipping_address")
            customer.save()
            order = Order.objects.filter(customer_id=customer.id).last()
            order_items = order.order_item_id.all()
            if not order_items:
                return redirect('ku-market-place:view_cart')
            order.status = random.choice(['Shipping', 'Delivery'])
            for order_item in order_items:
                order_item.product.quantity = order_item.product.quantity - order_item.quantity
                order_item.product.save()
            order.payment = payment
            order.save()
            order = Order.objects.create(
                customer_id=customer,
            )
            order.save()
            return redirect('ku-market-place:order_list')
        return redirect('ku-market-place:view_cart')


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        return redirect('ku-market-place:view_cart')

    def post(self, request, *args, **kwargs):
        form = CartForm(request.POST)
        product_id = kwargs.get("product_id")
        quantity = request.POST.get("quantity")

        if form:
            product = Product.objects.get(pk=product_id)
            order_item = OrderItem.objects.create(
                product=product,
                quantity=quantity,
                total_amount=product.productPrice * int(quantity),
            )
            order_item.save()
            try:
                customer = Customer.objects.get(user=request.user)
            except Customer.DoesNotExist:
                customer = Customer.objects.create(
                    user=request.user,
                )
                customer.save()
            order = Order.objects.filter(customer_id=customer.id).last()
            if order is None:
                order = Order.objects.create(
                    customer_id=Customer.objects.get(user=request.user.id),
                    total_amount=order_item.total_amount,
                )
                order.order_item_id.set([order_item])
                order.save()
                return redirect('ku-market-place:view_cart')
            try:
                order_item = order.order_item_id.get(product=order_item.product)
                order_item.quantity = int(order_item.quantity) + int(quantity)
                order_item.total_amount = (product.productPrice * int(quantity)) + order.total_amount
                order_item.save()
                return redirect('ku-market-place:view_cart')
            except OrderItem.DoesNotExist:
                order.order_item_id.add(order_item)
                order.save()
            order.total_amount = order.total_amount + (product.productPrice * int(quantity))
            order.save()

            # Redirect to a success page or the same page if needed
            return redirect('ku-market-place:view_cart')

        # If the form is not valid, you can re-render the same template with the form
        return redirect('ku-market-place:view_cart')


class RemoveFromCartView(View):
    def get(self, request, *args, **kwargs):
        return redirect('ku-market-place:view_cart')

    def post(self, request, *args, **kwargs):
        form = CartForm(request.POST)
        product_id = kwargs.get("product_id")
        quantity = request.POST.get("quantity")
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.filter(customer_id=customer.id).last()
        order_item = get_object_or_404(order.order_item_id, product_id=product_id)
        if form:
            if int(order_item.quantity) == int(quantity):
                order.total_amount -= order_item.total_amount
                order.order_item_id.remove(order_item)
                order.save()
                return redirect('ku-market-place:view_cart')
            elif order_item.quantity > int(quantity):
                order_item.quantity = order_item.quantity - int(quantity)
                order_item.total_amount = order_item.total_amount - (order_item.product.productPrice * int(quantity))
                order_item.save()
                order.total_amount = order.total_amount - (order_item.product.productPrice * int(quantity))
                order.save()
                return redirect('ku-market-place:view_cart')
        return redirect('ku-market-place:view_cart')


class OrderView(View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")
        order = get_object_or_404(Order, pk=order_id)
        order_items = order.order_item_id.all()
        return render(request, 'ku_market_place/order.html', {'order_items': order_items, 'order': order})