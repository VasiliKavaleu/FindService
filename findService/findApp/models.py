from django.db import models

class City(models.Model):
    '''Город'''
    name = models.CharField("Город", max_length=50)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

class CarModel(models.Model):
    '''Марка авто'''
    name = models.CharField("Марка авто", max_length=50)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Марка авто"
        verbose_name_plural = "Марки авто"

class Auto(models.Model):
    '''Авто'''
    url = models.CharField("Адрес", max_length=250, unique=True)
    title = models.CharField("Заголовок", max_length=250)
    description = models.TextField("Описание", blank=True)
    price = models.CharField("Цена", max_length=15)
    timestamp =models.DateField(auto_now_add=True)
    city = models.ForeignKey(City, verbose_name="Город", on_delete=models.CASCADE)
    carModel = models.ForeignKey(CarModel, verbose_name="Марка авто", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Авто"
        verbose_name_plural = "Автомобили"