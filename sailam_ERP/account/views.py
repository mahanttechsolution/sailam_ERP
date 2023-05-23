from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User
from account.forms import loginForm
def login(request):
    if request.method=="POST":
      form=loginForm(request.POST)
      if form.is_valid:
        username = request.POST["username"]
        password = request.POST["password"]
        print(username +" "+ password)
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
            loginform=loginForm()
            return render(request,'account/login.html',{'message':"Username Or Password Is Incorrect",'form':loginform})
    else:
     loginform=loginForm()
     return render(request,'account/login.html',{'form':loginform})


    
def register(request):
    return render(request,'account/register.html')
