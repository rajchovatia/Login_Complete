from django.contrib import admin

# Register your models here.
from login_register.models import TokenBlacklist,User_Otp

@admin.register(TokenBlacklist)
class tokenAdmin(admin.ModelAdmin) :
    list_display = ['user','token','expires_at']
    
@admin.register(User_Otp)
class userotpadmin(admin.ModelAdmin) :
    list_display = ['mobile','otp','validate_type','otp_expires']