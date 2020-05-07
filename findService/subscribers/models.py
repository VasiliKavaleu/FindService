from django.db import models
from findApp.models import City, CarModel

class Subscriber(models.Model):
    email = models.CharField('E-mail', max_length=100, unique=True)
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)
    carModel = models.ForeignKey(CarModel, verbose_name='Модель авто', on_delete=models.CASCADE)
    password = models.CharField('Пароль', max_length=100)
    is_activ = models.BooleanField('Получать рассылку?', default=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
