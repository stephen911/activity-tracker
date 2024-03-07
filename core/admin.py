from django.contrib import admin
from .models import Activity

# Register your models here.



@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name','status', 'created_at',)
