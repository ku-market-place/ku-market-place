from django.urls import path
from ku_market_place.views import HomePageView


app_name = "ku_market_place"
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
