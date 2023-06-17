from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate,login as auth_login,logout
from .models import User
from account.forms import loginForm

def login(request):
    if request.method=="POST":
      form=loginForm(request.POST)
      if form.is_valid:
        username = request.POST["username"]
        password = request.POST["password"]
        user= authenticate(username=username,password=password)
        if user is not None:
            print("Login done")
            auth_login(request,user)
            # write logic for rendering different users view
            context={
                user:user.get_username()
            }
            return render(request,'account/user.html',context)
        else:
    
            return render(request,'account/login.html',{'message':"Username Or Password Is Incorrect"})
    else:
     if request.user.is_authenticated:
        user=request.user
        context={
                user:user.get_username()
            }
        return render(request,'account/user.html',context)
     else:
        return render(request,'account/login.html')


    
def register(request):
    if request.method == 'POST':
       email=request.POST.get("inputEmail4")
       password=request.POST.get("inputPassword5")
       confirmpassword=request.POST.get("inputPassword6")
       firstname=request.POST.get("firstname")
       lastname=request.POST.get("lastname")
       print(email,firstname,lastname)
       
       if User.objects.filter(email=email).exists():
          return render(request,'account/register.html',{"message":"User Already Exist"})
          
       else:
          if password!=confirmpassword:
             return render(request,'account/register.html',{"message":"Password and Confirm Password is not matching"})
          else:
           created = User.objects.create_user(email=email,firstname=firstname,lastname=lastname,password=password)
           auth_login(request,created)
           context={
                created:created
            }
           return render(request,'account/user.html',context)
    else:
     return render(request,'account/register.html')

def logoutUser(request):
   logout(request)
   return redirect('login_account')