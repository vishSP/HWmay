from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from catalog.models import Category, Product, Blog


class IndexView(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all
        context['object_list'] = Product.objects.all
        return context


def contacts(request):
    return render(request, 'catalog/contacts.html')


class CardView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object']
        return context_data


class BlogView(ListView):
    model = Blog


class BlogCardView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'data', 'preview', 'is_active','date_create',)
    success_url = reverse_lazy('catalog:blog')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'data', 'preview', 'is_active','date_create',)
    success_url = reverse_lazy('catalog:blog')


class BlogDeleteView(DeleteView):
    model = Blog
    fields = ('title', 'data', 'preview', 'is_active', 'date_create',)
    success_url = reverse_lazy('catalog:blog')


def toggle_activity(request, slug):
    item = get_object_or_404(Blog, slug=slug)
    if item.is_active:
        item.is_active = False
    else:
        item.is_active = True

    item.save()

    return redirect(reverse('catalog:blog'))

