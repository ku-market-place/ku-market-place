from django.views import generic
from ku_market_place.models import Order

# Create your views here.


class HomePageView(generic.ListView):
    template_name = 'ku_market_place/index.html'
    context_object_name = 'order_lists'

    def get_queryset(self):
        return Order.objects.all()
