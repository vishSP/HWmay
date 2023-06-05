from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from catalog.forms import ProductForm, VersionForm
from catalog.models import Category, Product, Blog, Version


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
    fields = ('title', 'data', 'preview', 'is_active', 'date_create',)
    success_url = reverse_lazy('catalog:blog')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'data', 'preview', 'is_active', 'date_create',)
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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product')

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


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product')


class ProductDeleteView(DeleteView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product')
