from django.http import Http404
from django.urls import reverse
from django.views import generic, View
from ku_market_place.models import Product, Order, OrderItem, Customer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from ku_market_place.forms import CartForm, CheckOutForm


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
        form = CheckOutForm()
        # order = Order.objects.filter(customer_id=request.user.id)
        order = Order.objects.all()
        if order:
            # Get all order items related to the order
            order_items = OrderItem.objects.filter(id=order[0].id)
        else:
            # If there's no order, set order_items to an empty queryset or handle it accordingly
            order_items = OrderItem.objects.none()
        return render(request, 'ku_market_place/cart.html', {'order_items': order_items, 'form': form})


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        return redirect('ku-market-place:view_cart')

    def post(self, request, *args, **kwargs):
        form = CartForm(request.POST)
        product_id = kwargs.get("product_id")
        quantity = request.POST.get("quantity")

        if form.is_valid():

            # Assuming you have a Product model, get the product instance
            product = Product.objects.get(pk=product_id)

            # Assuming you have a Cart model, add the product to the cart
            # You may want to associate the product with the user and save it to the cart
            order_item = OrderItem.objects.create(
                product_id=product,
                quantity=quantity,
                total_amount=product.price * quantity,
            )
            order_item.save()
            try:
                order = Order.objects.get(customer_id=request.user.id)
                order.order_item_id.add(order_item)
                order.save()
            except Order.DoesNotExist:
                order = Order.objects.create(
                    customer_id=Customer.objects.get(pk=request.user.id),
                    order_item_id=order_item,
                    total_amount=order_item.total_amount,
                )
                order.save()
            print("success")

            # Redirect to a success page or the same page if needed
            return redirect('ku-market-place:view_cart')

        # If the form is not valid, you can re-render the same template with the form
        return redirect('ku-market-place:view_cart')
