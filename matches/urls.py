from django.urls import path

from matches.views import  HomeView

urlpatterns = [

    path('', HomeView.as_view(), name='homeview'),
]