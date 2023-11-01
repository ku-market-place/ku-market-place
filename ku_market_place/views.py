from django.views import generic
from ku_market_place.models import Order
from django.shortcuts import render


# Create your views here.


class HomePageView(generic.ListView):
    template_name = 'ku_market_place/index.html'
    context_object_name = 'order_lists'

    def get_queryset(self):
        return Order.objects.all()


def about(request):
    return render(request, 'ku_market_place/about.html')


def contact(request):
    return render(request, 'ku_market_place/contact.html')


def order_list(request):
    return render(request, 'ku_market_place/order_list.html')


def product(request):
    return render(request, 'ku_market_place/products.html')


def single_product(request):
    return render(request, 'ku_market_place/single-product.html')
