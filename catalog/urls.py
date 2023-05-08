from catalog.apps import CatalogConfig
from django.urls import path

from catalog.views import index, contacts, card

app_name= CatalogConfig.name
urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('index/<int:pk>/', card, name='card'),

]
