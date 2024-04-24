from django.contrib import admin

from .models import Invoice, LineItem,Recovery

admin.site.register(Invoice)
admin.site.register(LineItem)
admin.site.register(Recovery)
# Register your models here.
