from django.contrib import admin
from .models import Profile,Status
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name','email','mobile','batch','picture','is_active','created','updated']
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['profile','passing_year','title','description','created','updated']
    list_filter = ['profile','created']
