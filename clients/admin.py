from django.contrib import admin
from .models import Client,BusinessContact,FinancialContact

admin.site.register(Client)
admin.site.register(BusinessContact)
admin.site.register(FinancialContact)

