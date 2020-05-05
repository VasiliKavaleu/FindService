
from django.contrib import admin
from .models import City, Auto, CarModel, Site, Url

class AutoAdmin(admin.ModelAdmin):
    class Meta:
        model = Auto
    list_display = ('title', 'url', 'city', 'carModel', 'timestamp')


admin.site.register(City)
admin.site.register(Auto, AutoAdmin)
admin.site.register(CarModel)
admin.site.register(Site)
admin.site.register(Url)