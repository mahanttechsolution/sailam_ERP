import json
import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.files.storage import default_storage

from message.format import saveMessage
from .models import Color, Parcels,Jewellery, Type
from django.contrib.auth.decorators import login_required

@login_required
def inputView(request):
    typeData=Type.objects.all()
    colordata=Color.objects.all()
    result=[{'color':color.Name} for color in colordata]
    colorData = json.dumps(result)
    if request.method=="POST":
            form_id = request.POST['form_id']
            if form_id=='parcelform':
                user=request.user
                stkid=request.POST['stkid']
                crt=request.POST['crt']
                clarity=request.POST['clarity']
                desc=request.POST['desc']
                price=request.POST['price']
                color=request.POST['color']
                shape=request.POST['shape']
                file = request.FILES['img']
                print(stkid,crt,clarity,desc,price,color,shape,file)
                parcelobj=Parcels.objects.filter(Stk_Id=stkid).first()
                if not parcelobj:
                    parcel=Parcels.objects.create(Stk_Id=stkid,Crt=crt,Clarity=clarity,Desc=desc,Price=price,Color=color,Image=file,Shape=shape,CretedBy=user)
                    Color.objects.get_or_create(Name=color)
                    if parcel:
                        saveMessage("parcel",user,"Parcel",stkid,"Inserted",user.get_username())
                        return render(request,'parcels_jewellery/insertdata.html',{'message':'Parcel Inserted Successfully','dropdown_data':typeData,'colordata':colorData})
                    else:
                        return render(request,'parcels_jewellery/insertdata.html',{'errormessage':'Parcel Is Not Inserted','dropdown_data':typeData,'colordata':colorData})
                else: 
                   return render(request,'parcels_jewellery/insertdata.html',{'errormessage':'Parcel With StockId '+stkid+' Already Exist','dropdown_data':typeData,'colordata':colorData}) 
            elif form_id=='jewelleryform':
                user=request.user
                desc=request.POST['descjewel']
                price=request.POST['pricejewel']
                color=request.POST['colorjewel']
                file = request.FILES['imgjewel']
                jewelType=request.POST['type']
                jewelTypeObj=Type.objects.filter(Name=jewelType).first()
                print(desc,price,color,file,jewelType)
                jewellery=Jewellery.objects.create(Desc=desc,Price=price,Color=color,Image=file,CretedBy=user,Type=jewelTypeObj)
                if jewellery:
                    saveMessage("parcel",user,"Jewellery",jewellery.Id,"Inserted",user.get_username())
                    return render(request,'parcels_jewellery/insertdata.html',{'message':'Jewellery Inserted Successfully','dropdown_data':typeData,'colordata':colorData})
                else:
                    return render(request,'parcels_jewellery/insertdata.html',{'errormessage':'Jewellery Is Not Inserted','dropdown_data':typeData,'colordata':colorData})
    else:
        return render(request,'parcels_jewellery/insertdata.html',{'dropdown_data':typeData,'colordata':colorData})


def viewParcels(request):
    return render(request,'parcels_jewellery/parcels.html')

def viewJewellery(request):
    return render(request,'parcels_jewellery/jewellery.html')


def getParcelData(request):
    data = []
    parcelobj=Parcels.objects.filter(Isdeleted=False).values()
    for obj in parcelobj:
        parcel={}
        parcel['image']=obj['Image']
        parcel['description']=obj['Desc']
        parcel['color']=obj['Color']
        parcel['price']=obj['Price']
        parcel['shape']=obj['Shape']
        parcel['stkid']=obj['Stk_Id']
        parcel['crt']=obj['Crt']
        parcel['clarity']=obj['Clarity']
        data.append(parcel)
    return HttpResponse(json.dumps(data, indent = 4))

def getJewelleryData(request):
    data = []
    jewelleryobj=Jewellery.objects.filter(Isdeleted=False).values()
    for obj in jewelleryobj:
        jewellery={}
        jewellery['image']=obj['Image']
        jewellery['description']=obj['Desc']
        jewellery['color']=obj['Color']
        jewellery['price']=obj['Price']
        jewellery['type']=Type.objects.filter(Id=obj['Type_id']).first().Name
        data.append(jewellery)
    return HttpResponse(json.dumps(data, indent = 4))

@login_required
def allParcels(requets):
    return render(requets,'parcels_jewellery/viewParcels.html')

@login_required
def data_endpoint(request):
    parcelobj=Parcels.objects.filter().all()
    data = []
    for par in parcelobj:
        obj={}
        obj['Stk_Id']=par.Stk_Id
        obj['Crt']=par.Crt
        obj['Clarity']=par.Clarity
        obj['Desc']=par.Desc
        obj['Price']=par.Price
        obj['Color']=par.Color
        obj['Shape']=par.Shape
        if par.Isdeleted==True:
            obj['Actions']='<button type="button" class="btn btn-primary btn-xs dt-delete" value="Show">Show</button>'
        else:
            obj['Actions']='<button type="button" class="btn btn-danger btn-xs dt-delete" value="Hide">Hide</button>'
        data.append(obj)
        
    return JsonResponse(data, safe=False)


@login_required
def update_data_endpoint(request):
    if request.method == 'POST':
        user=request.user
        id = request.POST.get('id')
        column = request.POST.get('column')
        value = request.POST.get('value')
        parcelobj=Parcels.objects.get(Stk_Id=id)
        old_value=getattr(parcelobj,column)
        setattr(parcelobj, column, value)
        parcelobj.save()
        diff={}
        diff[column]={
                            'old_value': old_value,
                            'new_value': value
                     }
        saveMessage("parcel",user,"Parcel",id,"Updated",user.get_username(),**{'changes':str(diff)})
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def delete_data_endpoint(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user=request.user
        parcelobj=Parcels.objects.filter(Stk_Id=id).first()
        if parcelobj.Isdeleted==False:
            parcelobj.Isdeleted=True
            saveMessage("parcel",user,"Parcel",id,"Hided",user.get_username())
        else: 
            parcelobj.Isdeleted=False
            saveMessage("parcel",user,"Parcel",id,"Showed",user.get_username())
        parcelobj.UpdatedBy=user
        parcelobj.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def allJewellery(requets):
    return render(requets,'parcels_jewellery/viewJewellery.html')

@login_required
def jewellerydata_endpoint(request):
    jewelleryobj=Jewellery.objects.filter().all()
    data = []
    for par in jewelleryobj:
        obj={}
        obj['Id']=par.Id
        obj['Desc']=par.Desc
        obj['Price']=par.Price
        obj['Color']=par.Color
        if par.Isdeleted==True:
            obj['Actions']='<button type="button" class="btn btn-primary btn-xs dt-delete" value="Show">Show</button>'
        else:
            obj['Actions']='<button type="button" class="btn btn-danger btn-xs dt-delete" value="Hide">Hide</button>'
        data.append(obj)
    return JsonResponse(data, safe=False)

@login_required
def jewelleryupdate_data_endpoint(request):
    if request.method == 'POST':
        user=request.user
        id = request.POST.get('id')
        column = request.POST.get('column')
        value = request.POST.get('value')
        jewelleryobj=Jewellery.objects.get(Id=id)
        old_value=getattr(jewelleryobj,column)
        setattr(jewelleryobj, column, value)
        jewelleryobj.save()
        diff={}
        diff[column]={
                            'old_value': old_value,
                            'new_value': value
                     }
        saveMessage("parcel",user,"Jewellery",id,"Updated",user.get_username(),**{'changes':str(diff)})
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def jewellerydelete_data_endpoint(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user=request.user
        jewelleryobj=Jewellery.objects.filter(Id=id).first()
        if jewelleryobj.Isdeleted==False:
            jewelleryobj.Isdeleted=True
            saveMessage("parcel",user,"Jewellery",id,"Hided",user.get_username())
        else:
            jewelleryobj.Isdeleted=False
            saveMessage("parcel",user,"Jewellery",id,"Showed",user.get_username())
        jewelleryobj.UpdatedBy=user
        jewelleryobj.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
