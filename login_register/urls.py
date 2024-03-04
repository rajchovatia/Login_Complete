from django.urls import path
from login_register import views

urlpatterns = [
 path('',views.homepage,name="home"),
 path('register/',views.signuppage,name="register"),
 path('verify-otp/<str:mobile>/',views.verifyotp_page,name="varifyotp"),
 path('set-password/<str:mobile>/',views.setpasswordpage,name="setpassword"),
 path('login/',views.loginpage,name="login"),
 path('logout/',views.logoutpage,name="logout"),
]
