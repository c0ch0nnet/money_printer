from django.contrib import admin
from .models import Manager, Trade, Instrument

# Register your models here.

admin.site.register(Manager)
admin.site.register(Trade)
admin.site.register(Instrument)
