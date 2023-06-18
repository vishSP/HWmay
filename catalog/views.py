from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from rest_framework import permissions

from catalog.forms import ProductForm, VersionForm
from catalog.models import Category, Product, Blog, Version
from catalog.services import get_cache_categories


class IndexView(LoginRequiredMixin, TemplateView):
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
        context_data['all_categories'] = get_cache_categories()
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


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Blog
    fields = ('title', 'data', 'preview', 'is_active', 'date_create',)
    success_url = reverse_lazy('catalog:blog')


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'data', 'preview', 'is_active', 'date_create',)
    success_url = reverse_lazy('catalog:blog')


class BlogDeleteView(LoginRequiredMixin, DeleteView):
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product')
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):

        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404("Вы не являетесь владельцем этого товара")

        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product')
    permission_classes = [permissions.IsAuthenticated]


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product')
    permission_classes = [permissions.IsAuthenticated]
