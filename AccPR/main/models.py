from django.db import models


# Create your models here.
class Product(models.Model):
    code = models.CharField(max_length=255, verbose_name='Штрихкод')
    title = models.CharField(max_length=255, verbose_name='Наименование')
    count = models.IntegerField(verbose_name='Кол-во')
    cost_fs = models.FloatField(verbose_name='Розничная цена')
    cost_m = models.FloatField(verbose_name='Оптовая цена')
    profit = models.FloatField(verbose_name='Доход')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title
