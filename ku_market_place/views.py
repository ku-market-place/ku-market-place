from django.views import generic

# Create your views here.


class HomePageView(generic.ListView):
    template_name = 'ku_market_place/home.html'
    context_object_name = 'item_list'
