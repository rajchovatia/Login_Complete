from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User

class UserManager(BaseUserManager) :
    use_in_migrations = True
    
    def create_user(self,mobile, password, **extra_fields) :
        if not mobile :
            raise ValueError('mobile number is required !!')
        
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user
    
    
    def create_superuser(self,mobile, password, **extra_fields) :
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_superuser') is not True :
            raise ValueError('Super user is must have is_superuser true')
        
        return self.create_user(mobile, password, **extra_fields)
    