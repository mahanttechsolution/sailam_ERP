from datetime import datetime, timedelta, timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.models import User
from .models import Message

@login_required
def getMessage(requets):
    now = datetime.now(tz=timezone.utc)
    earlier = now - timedelta(hours=24)
    messObj=Message.objects.filter(Time__range=(earlier,now)).order_by('-Time').values()
    messages=[]
    for obj in messObj:
        mess={}
        mess['Message']=obj["Message"]
        time=obj["Time"]
        curr=datetime.now(tz=timezone.utc)
        diff=curr-time
        hours=int(diff.total_seconds()/3600)
        mess['Time']=hours
        messages.append(mess)
    # print(messages)
    return JsonResponse(messages, safe=False)

@login_required
def getLog(request):
    messObj=Message.objects.all().order_by('-Time').values()
    messages=[]
    for obj in messObj:
       mess={}
       mess['message_id']=obj["Id"]
       mess['message']=obj["Message"]
       sender=User.objects.filter(id=obj["Sender_id"]).first()
       mess['sender']=str(sender.first_name)+" "+str(sender.last_name)
       mess['date'] = datetime.strptime(str(obj["Time"]), '%Y-%m-%d %H:%M:%S.%f%z')
       if obj["Changes"] :
        mess['child_data']=obj["Changes"]
       messages.append(mess)
    return JsonResponse(messages, safe=False)


@login_required
def getLogView(request):
   return render(request,"message/logs.html")