from django.conf import settings
from django.core.cache import cache

from catalog.models import Category, Product


def get_cache_categories():
    if settings.CACHE_ENABLED:
        categories = cache.get('all_categories')
        if categories is None:
            categories = Category.objects.all()
            cache.set = ('all_categories', categories, 60 * 15)
            return categories
        else:
            return Category.objects.all()
