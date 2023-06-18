from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from django.urls import path

from catalog.views import contacts, CardView, BlogView, BlogCardView, IndexView, BlogCreateView, BlogUpdateView, \
    BlogDeleteView, toggle_activity, ProductCreateView, ProductUpdateView, ProductDeleteView
from users.models import User

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/auth/user/', User, name='admin'),
    path('contacts/', contacts, name='contacts'),
    path('index/<int:pk>/', cache_page(60)(CardView.as_view()), name='card'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('blog/<slug:slug>/', BlogCardView.as_view(), name='card_blog'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/update/<slug:slug>', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<slug:slug>', BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/toggle/<slug:slug>', toggle_activity, name='toggle_activity'),
    path('product/create/', ProductCreateView.as_view(), name='prod_create'),
    path('product/update/<int:pk>', never_cache(ProductUpdateView.as_view()), name='prod_update'),
    path('product/delete/<int:pk>', never_cache(ProductDeleteView.as_view()), name='prod_delete'),

]
