from django.db import models
from account.models import NewUser
# Create your models here.

class TokenBlacklist(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    expires_at = models.DateTimeField()



class User_Otp(models.Model) :
    
    VALIDATE_CHOICES = [("SIGNUP", 'Signup'),
                        ("LOGIN", 'Login'),
                        ("FORGET_PASSWORD", 'ForgetPassword'),]
    
    mobile = models.CharField(max_length=15)
    otp = models.IntegerField()
    validate_type = models.CharField(
        max_length=20,
        choices=VALIDATE_CHOICES,
        default="SIGNUP"
    )
    otp_expires= models.DateTimeField()
    
    