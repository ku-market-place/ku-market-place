from django.http import Http404
from django.urls import reverse
from django.views import generic, View
from ku_market_place.models import Product, Order, OrderItem, Customer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from ku_market_place.forms import CartForm, CheckOutForm
import random


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
                Q(productDisplayName__icontains=search_product)
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
        print("search_product is empty")
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
            form = CartForm()
        except Http404:
            messages.warning(
                request,
                f"Product ID {key} does not exist.❗️")
            return redirect("ku-market-place:product")

        return render(
            request,
            self.template_name,
            context={"product": product, "form": form},
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
        return render(request, 'ku_market_place/cart.html', {'order_items': order_items, 'form': form})

    def post(self, request, *args, **kwargs):
        form = CheckOutForm(request.POST)
        if form:
            customer = Customer.objects.get(user=request.user)
            order = Order.objects.filter(customer_id=customer.id).last()
            order.status = random.choice(['Shipping', 'Delivery', 'Complete'])
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
                order = Order.objects.get(customer_id=customer.id)
                order.order_item_id.add(order_item)
                order.save()
            except Order.DoesNotExist:
                order = Order.objects.create(
                    customer=Customer.objects.get(user=request.user),
                    order_item_id=order_item,
                    total_amount=order_item.total_amount,
                )
                order.save()
            print("success")

            # Redirect to a success page or the same page if needed
            return redirect('ku-market-place:view_cart')

        # If the form is not valid, you can re-render the same template with the form
        return redirect('ku-market-place:view_cart')
