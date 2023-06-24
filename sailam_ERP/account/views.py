from datetime import datetime, timedelta, timezone
from django.db.models import Count
from dateutil.relativedelta import relativedelta
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
from account.decorator import allowed_user
from .models import User,role
from django.db.models import Q
from inventory.models import inventory,InvoiceData
from parcels_jewellery.models import Jewellery,Parcels
from message.models import Inquiry
from account.forms import loginForm

total_diam=0
total_sell=0
live_diam=0
live_jewelery=0
live_parcel=0
inquirey=0

def setData():
   startdate = datetime.now(timezone.utc)
   enddate = startdate - relativedelta(years=1)
   global total_diam
   total_diam=inventory.objects.filter(Q(CreatedOn__gte=enddate) & Q(CreatedOn__lte=startdate)).count()
   global total_sell
   total_sell=inventory.objects.filter(Q(CreatedOn__gte=enddate) & Q(CreatedOn__lte=startdate),InvoiceMade=True).count()
   global live_diam
   live_diam=inventory.objects.filter(InvoiceMade=False).count()
   global live_jewelery
   live_jewelery=Jewellery.objects.filter(Isdeleted=False).count()
   global live_parcel
   live_parcel=Parcels.objects.filter(Isdeleted=False).count()
   global inquirey
   inquirey=Inquiry.objects.filter(Q(date__gte=enddate) & Q(date__lte=startdate)).count()

   data = inventory.objects.filter(Q(CreatedOn__gte=enddate) & Q(CreatedOn__lte=startdate)).values('Location').annotate(count=Count('STK_ID'))
   data1 = inventory.objects.filter(Q(CreatedOn__gte=enddate) & Q(CreatedOn__lte=startdate),InvoiceMade=True).values('Location').annotate(count=Count('STK_ID'))
   global labels 
   labels= [entry['Location'] for entry in data]
   global bought_data
   bought_data = [entry['count'] for entry in data]
   global sold_data
   sold_data = [entry['count'] for entry in data1]

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
            print(user.groups.all().values()[0]['name'])
            # write logic for rendering different users view
            setData()
            context={
                'user':user,
                'total_diam':total_diam,
                'total_sell':total_sell,
                'live_diam':live_diam,
                'live_jewelery':live_jewelery,
                'live_parcel':live_parcel,
                'inquirey':inquirey,
                'labels': labels,
                'bought_data': bought_data,
                'sold_data': sold_data
            }
            return render(request,'dashboard.html',context)
        else:
            return render(request,'account/login.html',{'message':"Username Or Password Is Incorrect"})
    else:
     if request.user.is_authenticated:
        user=request.user
        setData()
        context={
                'user':user,
                'total_diam':total_diam,
                'total_sell':total_sell,
                'live_diam':live_diam,
                'live_jewelery':live_jewelery,
                'live_parcel':live_parcel,
                'inquirey':inquirey,
                'labels': labels,
                'bought_data': bought_data,
                'sold_data': sold_data
            }
        return render(request,'dashboard.html',context)
     else:
        return render(request,'account/login.html')


def register(request):
    if request.method == 'POST':
       email=request.POST.get("inputEmail4")
       password=request.POST.get("inputPassword5")
       confirmpassword=request.POST.get("inputPassword6")
       firstname=request.POST.get("firstname")
       lastname=request.POST.get("lastname")
       mobile=request.POST.get("mobile")
    #    print(email,firstname,lastname)
       
       if User.objects.filter(email=email).exists():
          return render(request,'account/register.html',{"message":"User Already Exist"})
          
       else:
          if password!=confirmpassword:
             return render(request,'account/register.html',{"message":"Password and Confirm Password is not matching"})
          else:
           created = User.objects.create_user(email=email,firstname=firstname,lastname=lastname,password=password,mobile=mobile)
           auth_login(request,created)
           user=request.user
           setData()
           context={
                'user':user,
                'total_diam':total_diam,
                'total_sell':total_sell,
                'live_diam':live_diam,
                'live_jewelery':live_jewelery,
                'live_parcel':live_parcel,
                'inquirey':inquirey,
                'labels': labels,
                'bought_data': bought_data,
                'sold_data': sold_data
            }
           return render(request,'dashboard.html',context)
    else:
     return render(request,'account/register.html')

@login_required
def logoutUser(request):
   logout(request)
   return redirect('login_account')

# @allowed_user(allowed_roles=['Admin','Salesmen'])
def fetch_data(request):
    startdate = datetime.now(timezone.utc)
    enddate = startdate - relativedelta(years=1)
    # start = request.GET.get('start')
    # end = request.GET.get('end')

    # Calculate the count of entries in the Inventory table for each 1-month interval
    intervals = []
    current_date = enddate
    while current_date+ relativedelta(months=1) < startdate:
        next_date = current_date + relativedelta(months=1)
        buy = inventory.objects.filter(Q(CreatedOn__gte=current_date) & Q(CreatedOn__lte=next_date)).count()
        sell= inventory.objects.filter(Q(CreatedOn__gte=current_date) & Q(CreatedOn__lte=next_date), InvoiceMade=True).count()
        intervals.append({
            'start': current_date.date().strftime('%B'),
            'end': next_date.date().strftime('%B'),
            'buy': buy,
            'sell':sell,
        })
        current_date = next_date

    buy = inventory.objects.filter(Q(CreatedOn__gte=current_date) & Q(CreatedOn__lte=startdate)).count()
    sell= inventory.objects.filter(Q(CreatedOn__gte=current_date) & Q(CreatedOn__lte=startdate), InvoiceMade=True).count()
    intervals.append({
        'start': current_date.date().strftime('%B'),
        'end': startdate.date().strftime('%B'),
        'buy': buy,
        'sell':sell,
    })

    # Prepare the data for chart rendering
    data = {
        'x': [f"{interval['start']}" for interval in intervals],
        'buy': [interval['buy'] for interval in intervals],
        'sell': [interval['sell'] for interval in intervals]
    }

    return JsonResponse(data,safe=False)

@login_required
def getProfileView(request):
   return render(request,'account/profile.html')


@login_required
def getUsers(request):
   users=[]
   userobj=User.objects.all().values()
   for obj in userobj:
      user={}
      user["name"]=obj['first_name']+" "+obj['last_name']
      user['username']=obj['email']
      user['date']=str(obj['date_joined'].date())
      user['mobile']=obj['mobile']
      user['role']=role.objects.filter(role_id=obj['role_id']).first().role_name
      user['isActive']=obj['is_active']
      users.append(user)

   return JsonResponse(users,safe=False)
