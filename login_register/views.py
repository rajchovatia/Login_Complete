from django.shortcuts import render,redirect
from account.models import NewUser
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from datetime import timedelta
from django.utils import timezone
from login_register.models import TokenBlacklist,User_Otp
from rest_framework_simplejwt.tokens import RefreshToken
import random
from datetime import datetime
# import requests

def homepage(request) :
    return render(request,"index.html")


def loginpage(request) :
    
    if request.method == "POST" :
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        
        if not NewUser.objects.filter(mobile=mobile).exists() :
            messages.error(request,'Invalid Mobile Number !!')
            return redirect(request.path)
        
        user = authenticate(mobile=mobile,password=password)
        
        if TokenBlacklist.objects.filter(user__mobile=mobile).exists():
            messages.warning(request, 'User is already logged in!')
            # print("User Already Exists!!")
            return redirect(request.path)
        
        if user is None :
            messages.error(request, 'Password Incorrect Try Again !!')
            return redirect(request.path)
        else :
            login(request,user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            # print("Access Token is->",access_token)
            token_expiry = timezone.now() + timedelta(minutes=1)  # 5 minutes expiry
            # print("Time Zone is ->",timezone.now())
            TokenBlacklist.objects.create(user=user, token=access_token, expires_at=token_expiry)
            return redirect('home')

    return render(request,"login_page.html")


def logoutpage(request) :
    user = request.user
    token_entry = TokenBlacklist.objects.filter(user=user).first()
    if token_entry:
        token_entry.delete()
    logout(request)
    return redirect('home')


def generate_otp():
    otp = random.randint(1000,9999)
    # request.session['otp'] = otp
    return otp

def signuppage(request) :
    if request.method == "POST" :
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        mobile = request.POST.get('mobile')
        
        print(firstname,mobile)
        
        if NewUser.objects.filter(mobile=mobile).exists() :
            messages.error(request,'Mobile alredy exists !!')   
            return redirect('register')
        
        otp = generate_otp()
        print(f"Otp is ->{otp} and type ->{type(otp)}")
        # validate_type = User_Otp.SIGNUP  # or whichever type you want
        expires_at = datetime.now() + timedelta(minutes=5)  # Set expiration time, e.g., 10 minutes from now

        if mobile:
            data = User_Otp.objects.create(mobile=mobile,otp=otp,validate_type="SIGNUP",otp_expires=expires_at)
            data.save()
            print("OTP IS->",otp)
            # New_mobile = "+91" + mobile                                                                          
            # url = f'https://2factor.in/API/V1/API KEY ADD/SMS/{New_mobile}/{otp}/OTP1'
                                                                                                    
            # res = requests.get(url)                                                            
            # print(res.status_code)                                                             
                                                                                                    
            # if res.status_code == 200:                                                         
            #     messages.success(request, "You have successfully signed up! An OTP has been sent to your mobile.")
            #     print("Yes OTP Successfully ")                                                         
            # else:                                                                                      
            #     print("OTP is not Sent Due to Some Error ", res.status_code)
            
            user = NewUser.objects.create(first_name=firstname,
                                      last_name=lastname,
                                      mobile=mobile,)
            user.save()
        return redirect('varifyotp',mobile=mobile)        
    return render(request,"signup_page.html")


def verifyotp_page(request,mobile) :
    
    data = {
        'mobile': mobile
    }
    
    if request.method == "POST":
        user_1 = request.POST.get('digit1')
        user_2 = request.POST.get('digit2')
        user_3 = request.POST.get('digit3')
        user_4 = request.POST.get('digit4')
        user_otp = f"{user_1}{user_2}{user_3}{user_4}"
        
        current_time = datetime.now()
        expired_entries = User_Otp.objects.filter(otp_expires__lt=current_time)
        expired_entries.delete()
        
        obj = User_Otp.objects.filter(mobile=mobile)
        print("Object is ->",obj)
        if not obj:
            messages.error(request, "OTP has expired. Please request a new OTP.")
            user = NewUser.objects.get(mobile=mobile)
            user.delete()
            
            return redirect('register')
        stored_otp = obj[0].otp
        
        if user_otp == str(stored_otp):
            # print("Otp Mach Success fully !!")
            obj.delete()
            # print("Data Successfully Delete !!!!!")
            return redirect('setpassword',mobile)
        else :
            messages.error(request, "Invalid OTP !!")
            return redirect(request.path)
        
    return render(request,"otp_varification.html",data)

def setpasswordpage(request,mobile) :
    try:
        user = NewUser.objects.get(mobile=mobile)
        if request.method == "POST":
            password = request.POST.get('password')
            confirmpassword = request.POST.get('confirmpassword')
            # print(password)
            # print(confirmpassword)
            if password == confirmpassword :
                user.set_password(password)
                user.save()
                # messages.success(request, 'Your password has been successfully Set')
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                print("Access Token is->",access_token)
                token_expiry = timezone.now() + timedelta(minutes=5)  # 5 minutes expiry
                print("Time Zone is ->",timezone.now())
                TokenBlacklist.objects.create(user=user, token=access_token, expires_at=token_expiry)
                login(request,user)
                return redirect('/')
            else:
                # Passwords do not match
                messages.error(request, 'Password and confirm password do not match. Please try again.')
                return redirect(request.path)
        data = {
            "mobile" : mobile
        }
    except NewUser.DoesNotExist:
        # Handle case where user with given mobile number doesn't exist
        messages.error(request, 'User with the provided mobile number does not exist.')
        user.delete()
        return redirect('/')
    return render(request,"Create_Password.html",data)

