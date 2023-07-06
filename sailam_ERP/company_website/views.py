from django.shortcuts import render
from inventory.models import inventory
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
def stocks(request):
    if request.method == "POST":
        flag = request.POST["flag"]

    else:
        try:
            flag = request.GET["flag"]
            if flag == "non-gia":
                stocks = inventory.objects.filter(IsHide=False).exclude(Q(GIA_NO__isnull=False)|Q(GIA_NO__exact='')| Q(GIA_NO='None')).values('STK_ID','CRT','SHAPE','COLOR','PRICE','CLARITY','SYM')
                print(stocks)
                context = {"status": "0", "stocks": list(stocks)}
                # print(context)
                return JsonResponse(context)
        except Exception as e:
            print("------------->", e)
            stocks = inventory.objects.filter(IsHide=False)
            context = {"stocks": stocks}
            return render(request, "company/all_details.html", context)

def filter_data(request):
    shape = request.POST.getlist("shape[]")
    color = request.POST.getlist("color[]")
    location = request.POST.getlist("location[]")
    symmetry = request.POST.getlist("symmetry[]")
    polish = request.POST.getlist("polish[]")
    clarity = request.POST.getlist("clarity[]")
    fancy = request.POST.getlist("fancy[]")
    weight = request.POST.getlist("weight[]")
    
    filter_color = Q()
    filter_shape = Q()
    filter_location = Q()
    filter_symmetry = Q()
    filter_polish = Q()
    filter_clarity = Q()
    filter_fancy = Q()
    filter_weight = Q()

    for value in shape:
        if value == "ALL":
            break
        else:
            filter_shape |= Q(SHAPE__icontains=value)

    for value in weight:
        if value == "ALL":
            break
        else:
            if value == "0.30":
                filter_weight |= Q(CRT__lte=0.30)
            if value == "0.31":
                filter_weight |= Q(CRT__gte=0.31,CRT__lte=0.5)
            if value == "0.51":
                filter_weight |= Q(CRT__gte=0.51,CRT__lte=1)
            if value == "1":
                filter_weight |= Q(CRT=1)
            if value == "1.00":
                filter_weight |= Q(CRT__gte=1,CRT__lte=3)
            if value == "3.00":
                filter_weight |= Q(CRT__gte=3,CRT__lte=5)
            if value == "5.00":
                filter_weight |= Q(CRT__gte=5)
            
    for value in color:
        if value == "ALL":
            break
        else:
            filter_color |= Q(COLOR__icontains=value)

    for value in fancy: 
        if value == "ALL":
            break
        else:
            filter_fancy |= Q(COLOR__icontains=value)

    for value in clarity: 
        if value == "ALL":
            break
        else:
            filter_clarity |= Q(CLARITY__icontains=value)

    for value in symmetry: 
        if value == "ALL":
            break
        else:
            filter_symmetry |= Q(SYM__icontains=value)

    for value in polish: 
        if value == "ALL":
            break
        else:
            filter_polish |= Q(POL__icontains=value)
            
    for value in location: 
        if value == "ALL":
            break
        else:
            filter_location |= Q(Location__icontains=value)

    data = inventory.objects.filter(filter_shape,filter_weight,filter_color,filter_clarity,filter_symmetry,filter_polish,filter_location,IsHide=False).values('GIA_NO','STK_ID','CRT','SHAPE','COLOR','PRICE','CLARITY','SYM','Scan_Id')
 
    context = {"status": "1","data":list(data)}
    return JsonResponse(context)