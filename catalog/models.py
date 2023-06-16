from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='название категории')
    category_description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('category_name',)


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.CharField(max_length=50, verbose_name='описание')
    image = models.ImageField(upload_to='product', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.IntegerField(verbose_name='цена')
    date_create = models.DateField(auto_now_add=True, verbose_name='дата создания')
    date_last = models.DateField(verbose_name='дата последнего изменения ')

    is_published = models.BooleanField(default=False, verbose_name='признак публикации')

    def __str__(self):
        return f'{self.name}{self.price}{self.category}'

    def delete(self, *args, **kwargs):
        self.save()

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="название статьи")
    slug = models.CharField(max_length=150, verbose_name="человекопонятный url")
    data = models.TextField(verbose_name='cодержимое статьи')
    preview = models.ImageField(upload_to='blog', verbose_name='изображение', **NULLABLE)
    date_create = models.DateField(verbose_name='дата создания')
    views_count = models.IntegerField(default=0, verbose_name='счетчик просмотров')

    is_active = models.BooleanField(default=True, verbose_name='активная статья')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('title',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    number_version = models.IntegerField(verbose_name='номер версии')
    title_version = models.CharField(max_length=100, verbose_name='название версии')

    is_active = models.BooleanField(default=True, verbose_name='неактивная версия')

    def __str__(self):
        return self.title_version

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
        ordering = ('title_version',)
