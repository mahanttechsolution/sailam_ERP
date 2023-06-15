import json
import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.files.storage import default_storage
from .models import Color, Parcels,Jewellery, Type

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


def allParcels(requets):
    return render(requets,'parcels_jewellery/viewParcels.html')


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


def update_data_endpoint(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        column = request.POST.get('column')
        value = request.POST.get('value')
        parcelobj=Parcels.objects.get(Stk_Id=id)
        setattr(parcelobj, column, value)
        parcelobj.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def delete_data_endpoint(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user=request.user
        parcelobj=Parcels.objects.filter(Stk_Id=id).first()
        if parcelobj.Isdeleted==False:
            parcelobj.Isdeleted=True
        else: 
            parcelobj.Isdeleted=False
        parcelobj.UpdatedBy=user
        parcelobj.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def allJewellery(requets):
    return render(requets,'parcels_jewellery/viewJewellery.html')


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


def jewelleryupdate_data_endpoint(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        column = request.POST.get('column')
        value = request.POST.get('value')
        jewelleryobj=Jewellery.objects.get(Id=id)
        setattr(jewelleryobj, column, value)
        jewelleryobj.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def jewellerydelete_data_endpoint(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user=request.user
        jewelleryobj=Jewellery.objects.filter(Id=id).first()
        if jewelleryobj.Isdeleted==False:
            jewelleryobj.Isdeleted=True
        else:
            jewelleryobj.Isdeleted=False
        jewelleryobj.UpdatedBy=user
        jewelleryobj.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
