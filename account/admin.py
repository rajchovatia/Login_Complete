from django.contrib import admin

# Register your models here.
from account.models import NewUser

class NewUserAdmin(admin.ModelAdmin) :
    list_display = ['mobile','user_bio','is_verified','email']

admin.site.register(NewUser,NewUserAdmin)