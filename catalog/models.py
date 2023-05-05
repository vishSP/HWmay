from django.db import models

# Create your models here.
NULLABLE = {'blank': True, 'null': True}

class Category(models.Model):
    category_name = models.CharField(max_length=50,verbose_name='название категории')
    category_description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.category_name



class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.CharField(max_length=50, verbose_name='описание')
    image = models.ImageField(upload_to='product', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='категория')
    price = models.IntegerField(verbose_name='цена')
    date_create = models.DateField(verbose_name='дата создания')
    date_last = models.DateField(verbose_name='дата последнего изменения ')

    def __str__(self):
        return f'{self.name}{self.price}{self.category}'


