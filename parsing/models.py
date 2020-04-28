from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from .choices import STATUS_CHOICES

class Operator(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Оператор'
        verbose_name_plural = 'Оператори'
        ordering = ['name']

STATUS_CHOICES = (
    (1, ("Завантажений")),
    (2, ("Обробляється")),
    (3, ("Оброблений")),
    (4, ("Оброблений частково")),
    (5, ("Помилка"))
)

class File(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=r'workflow/%Y-%m-%d')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1,)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, related_name='uploaded_by', default=None, null=True)
    operator = models.ForeignKey(Operator, on_delete=models.DO_NOTHING, related_name='file_operator', default=None, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файли'
        ordering = ['uploaded_at']

class Region(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Області'
        ordering = ['name']

class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Місто'
        verbose_name_plural = 'Міста'
        ordering = ['name']

class CityArea(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Район міста'
        verbose_name_plural = 'Райони міста'
        ordering = ['name']

class MediaType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип носія'
        verbose_name_plural = 'Типи носіїв'
        ordering = ['name']

class BoardSize(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Розмір площини'
        verbose_name_plural = 'Розміри площин'
        ordering = ['name']

class Side(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сторона'
        verbose_name_plural = 'Сторони'
        ordering = ['name']

class Board(models.Model):
    kod = models.CharField(max_length=20, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, related_name='regions', default=None, null=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, related_name='cities', default=None, null=True)
    city_area = models.ForeignKey(CityArea, on_delete=models.DO_NOTHING, related_name='city_areas', default=None, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    media_type = models.ForeignKey(MediaType, on_delete=models.DO_NOTHING, related_name='media_types', default=None, null=True)
    size = models.ForeignKey(BoardSize, on_delete=models.DO_NOTHING, related_name='sizes', default=None, null=True)
    side = models.ForeignKey(Side, on_delete=models.DO_NOTHING, related_name='sides', default=None, null=True)
    light = models.BooleanField(default=None, blank=True, null=True)
    ots = models.IntegerField(blank=True, null=True)
    grp = models.FloatField(blank=True, null=True)
    kod_doors = models.IntegerField(blank=True, null=True)
    operator = models.ForeignKey(Operator, on_delete=models.DO_NOTHING, related_name='regions', default=None, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.kod

    class Meta:
        verbose_name = 'Площина'
        verbose_name_plural = 'Площини'
        ordering = ['created']

class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статуси'
        ordering = ['name']

class Month(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Місяць'
        verbose_name_plural = 'Місяці'
        ordering = ['id']

class Year(models.Model):
    name = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рік'
        verbose_name_plural = 'Роки'
        ordering = ['id']

class StatusPrice(models.Model):
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING, related_name='boards', default=None, null=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='statuses', default=None, null=True)
    price = models.FloatField(blank=True, null=True)
    month = models.ForeignKey(Month, on_delete=models.DO_NOTHING, related_name='months', default=None, null=True)
    year = models.ForeignKey(Year, on_delete=models.DO_NOTHING, related_name='years', default=None, null=True)

    # def __str__(self):
    #     return self.price

    class Meta:
        verbose_name = 'Статус, Прайс'
        verbose_name_plural = 'Статуси, Прайси'
        ordering = ['id']


# class StatusPrice(models.Model):
#     board = models.ForeignKey(Board, on_delete=models.DO_NOTHING,related_name='board', default=None, null=True)
#     year = models.IntegerField(blank=True, null=True)
#     jan_s = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='january_status', default=None, null=True)
#     jan_p = models.FloatField(blank=True, null=True)
#     feb_s = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='february_status', default=None, null=True)
#     feb_p = models.FloatField(blank=True, null=True)
#     mar_s = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='march_status', default=None, null=True)
#     mar_p = models.FloatField(blank=True, null=True)
#     apr_s = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='april_status', default=None, null=True)
#     apr_p = models.FloatField(blank=True, null=True)
#     may_s = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='may_status', default=None, null=True)
#     may_p = models.FloatField(blank=True, null=True)
#     jun_s = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='june_status', default=None, null=True)
#     jun_p = models.FloatField(blank=True, null=True)
#     jul_s = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='july_status', default=None, null=True)
#     jul_p = models.FloatField(blank=True, null=True)
#     aug_s = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='august_status', default=None, null=True)
#     aug_p = models.FloatField(blank=True, null=True)
#     sep_s = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='september_status', default=None, null=True)
#     sep_p = models.FloatField(blank=True, null=True)
#     oct_s = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='october_status', default=None, null=True)
#     oct_p = models.FloatField(blank=True, null=True)
#     nov_s = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='november_status', default=None, null=True)
#     nov_p = models.FloatField(blank=True, null=True)
#     dec_s = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='december_status', default=None, null=True)
#     dec_p = models.FloatField(blank=True, null=True)


