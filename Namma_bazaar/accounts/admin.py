from django.contrib import admin
from accounts.models import Accounts
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class Accountadmin (UserAdmin):
    list_display=['email','first_name','last_name','username','date_joined','last_login','is_active',]
    list_display_links=['email','first_name','last_name']
    readonly_fields=['date_joined','last_login']
    ordering=['-date_joined']

    #these fields are required by deafault when we create custom admin panel
    list_filter=()
    filter_horizontal=()
    fieldsets=()

admin.site.register(Accounts,Accountadmin)
