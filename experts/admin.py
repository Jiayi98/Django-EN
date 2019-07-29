

# Register your models here.
from django.contrib import admin
from .models import ExpertComments, ExpertInfo, WorkExp

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(ExpertComments)
#admin.site.register(ExpertInfo)
admin.site.register(WorkExp)

@admin.register(ExpertInfo)
class ExpertInfoAdmin(admin.ModelAdmin):
    list_display = ('ename','emobile','eemail','etrade','esubtrade',
                   'elocation','eqq','estate','ecomefrom',
                    'eremark','addtime')
    list_filter = ('etrade','esubtrade')
    search_fields = ('etrade','esubtrade','addtime')
    ordering = ('-addtime',)