import datetime
import sys
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, JsonResponse
import requests
import json
from django.conf import settings

from  message.format import saveMessage
from  account.models import User
from .models import Invoice, InvoiceData, Location, Tally, TallyData, inventory,Client,Memo,MemoData
from .models import inventory, Video
from .forms import VideoForm
import qrcode
import os
from io import BytesIO
import qrcode
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlretrieve
from django.core.paginator import Paginator

from django.db import connection
from num2words import num2words
from io import BytesIO
import qrcode
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.decorators import login_required
# Create your views here.

BASE_DIR = settings.BASE_DIR


def loadGiaData(request):
    if request.method == "POST":
        url_end_point = "https://api.reportresults.gia.edu/"
        report_number = request.POST.get("gianumber")
        file1 = open("static/query/master.txt")
        content = file1.read()
        query = {"query": content, "variables": {"reportNumber": report_number}}

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "64112d47-a247-4259-a9d0-a402e186f4a8",
        }

        response = requests.post(url_end_point, data=json.dumps(query), headers=headers)
        data = response.json()
    return HttpResponse(json.dumps(data), content_type="application/json")


def compare_objects(old_obj, new_obj, allowkeys):
    differences = {}

    for attr_name, new_value in new_obj.__dict__.items():
            if attr_name in allowkeys:
                if hasattr(old_obj, attr_name):
                    old_value = getattr(old_obj, attr_name)
                    
                    if old_value != new_value:
                        differences[attr_name] = {
                            'old_value': old_value,
                            'new_value': new_value
                        }
    return differences

def trigfunction(stk_id,match_id):
   c=connection.cursor()
   try:
      c.execute("BEGIN")
      c.callproc("group_rows",(stk_id,match_id))
      result=c.fetchall()
      c.execute("COMMIT")
   finally:
      c.close()

def trigGetDistinctGroup():
   c=connection.cursor()
   try:
      c.execute("BEGIN")
      c.callproc("get_distinct_grouped_ids")
      result=c.fetchall()
      c.execute("COMMIT")
   finally:
      c.close()
   return result

@login_required
def getGroupView(request):
    return render(request,"inventory/match.html")

@login_required
def getGroupData(request):
    if request.method=="GET":
        result=trigGetDistinctGroup()
        data=[]
        for tuples in result:
            group={}
            tuple=tuples[0]
            ids=tuple.split(',')
            size = len(ids)
            if size==1:
               continue
            group["child_data"]=[]
            cnt=0
            for i in range(0,size):
               inv={}
               invobj=inventory.objects.filter(STK_ID=ids[i],InvoiceMade=False,IsHide=False).first()
               if invobj:
                if  cnt==0:
                    group["stk_id"]=invobj.STK_ID
                    group["gia"]=invobj.GIA_NO
                    group["desc"]="<b>Shape:</b> "+invobj.SHAPE+", <b>Color:</b> "+invobj.COLOR+", <b>Clarity:</b> "+invobj.CLARITY
                    group["weight"]=invobj.CRT
                    group["measurement"]=invobj.MESUREMNT
                    group["price"]=invobj.PRICE
                else:
                    inv["stk_id"]=invobj.STK_ID
                    inv["gia"]=invobj.GIA_NO
                    inv["desc"]="<b>Shape:</b> "+invobj.SHAPE+", <b>Color:</b> "+invobj.COLOR+", <b>Clarity:</b> "+invobj.CLARITY
                    inv["weight"]=invobj.CRT
                    inv["measurement"]=invobj.MESUREMNT
                    inv["price"]=invobj.PRICE
                    group["child_data"].append(inv)
                cnt+=1
            data.append(group)
        # print(data)
    return HttpResponse(json.dumps(data))


@login_required
def insertDiamond(request):
    if request.method == "POST":
        user = request.user
        stkid = request.POST.get("stkid")
        shape = request.POST.get("shape")
        color = request.POST.get("color")
        clarity = request.POST.get("clarity")
        polish = request.POST.get("polish")
        symmetry = request.POST.get("symmetry")
        cut = request.POST.get("cut")
        fluorescence = request.POST.get("fluorescence")
        mesurement = request.POST.get("mesurement")
        depth = request.POST.get("depth")
        table = request.POST.get("table")
        giano = request.POST.get("giano")
        remark = request.POST.get("remark")
        price = request.POST.get("price")
        crt = request.POST.get("crt")
        desc = request.POST.get("desc")
        location=request.POST.get("location")
        matchid=request.POST.get("dropdown")
        scan = 0

        if inventory.objects.last() == None:
            scan = encrypt(1)
        else:
            scan = encrypt(inventory.objects.last().Id)
        # print(scan)
        exist = inventory.objects.filter(GIA_NO=giano,STK_ID=stkid).values()
        if not exist:
            stock = inventory.objects.create(
                SHAPE=shape,
                COLOR=color,
                CLARITY=clarity,
                POL=polish,
                SYM=symmetry,
                CUT=cut,
                FLO_COL=fluorescence,
                MESUREMNT=mesurement,
                DEPTH=depth,
                TABLE=table,
                GIA_NO=giano,
                REMARK=remark,
                PRICE=price,
                STK_ID=stkid,
                CRT=crt,
                DESCRIPTION=desc,
                CretedBy=user,
                Scan_Id=scan,
                Location=location,
                Match=matchid,
            )
            Location.objects.get_or_create(Name=location)
            if stock:
                if not matchid:
                 trigfunction(stkid,stkid)
                else:
                 trigfunction(stkid,matchid)
                saveMessage("inventory",user,"Inventory",stkid,"Inserted",user.get_username())
                link = request.POST["link"]
                if link:
                    request.POST._mutable = True
                    if link.endswith(".jpg"):
                        i = link.rfind("/")
                        did = link[i + 1 : -4]
                    else:
                        did = link.split("=")[1]
                    request.POST["link"] = did
                # print(request.POST)
                form = VideoForm(request.POST, request.FILES)
                if form.is_valid():
                    #    saving video and image to media
                    if form.data['image'] or form.data['file'] or form.data['link']:
                        video = form.save(commit=False)
                        video.id_inv = stock
                        video.save()
                    form = VideoForm()
                    # sid, weight, shape, color, purity
                    #    generating qr code
                    path = generate_sticker(
                        scan,
                        sid=stkid,
                        weight=crt,
                        shape=shape,
                        color=color,
                        purity=clarity,
                        gia=giano,
                    )
                    # path = generate_qr_code(scan)
                    return render(
                        request,
                        "inventory/inventory.html",
                        {
                            "message": "Data Inserted Successfully!",
                            "form": form,
                            "qr_code_path": path,
                        },
                    )
                else:
                    form = VideoForm()
                    return render(
                        request,
                        "inventory/inventory.html",
                        {
                            "errormessage": "Video and Photo is not uploaded",
                            "form": form,
                        },
                    )
        else:
            form = VideoForm()
            return render(
                request,
                "inventory/inventory.html",
                {"errormessage": "Data Is Already Present", "form": form},
            )
    else:
        locationdata=Location.objects.all()
        result=[{'location':location.Name} for location in locationdata]
        locationData = json.dumps(result)
        form = VideoForm()
        return render(request, "inventory/inventory.html", {'form': form,'locationdata':locationData})

@login_required
def viewStock(request):
    try:
        page_number = request.GET["page"]
    except:
        page_number = 1
    stocks = inventory.objects.all()
    p = Paginator(stocks, 10)
    page_obj = p.get_page(page_number)
    last_page = p.num_pages
    context = {"stocks": page_obj, "last_page": last_page}
    return render(request, "inventory/viewinventory.html", context)


def StockInfo(request):
    stocks = inventory.objects.all()
    context = {"stocks": stocks}
    return render(request, "inventory/all_details.html", context)


@login_required
def retStk(request):
    stocks = inventory.objects.all().values()
    data=[]
    for row in stocks:
     data.append(row["STK_ID"])
    return HttpResponse(json.dumps(data))

@login_required
def updateInventory(request):
    if request.method=="POST":
        user=request.user
        data=json.loads(request.body)
        stk_id=data['stk_id']
        weight=data['weight']
        measurement=data['measurement']
        clarity=data['clarity']
        price=data['price']
        color=data['color']
        polish=data['polish']
        symmetry=data['symmetry']
        cut=data['cut']
        fluorescence=data['fluorescence']
        depth=data['depth']
        table=data['table']
        remarks=data['remarks']
        invobj=inventory.objects.filter(STK_ID=stk_id).first()
        prev=inventory.objects.filter(STK_ID=stk_id).first()
        allow=['CRT','MESUREMNT','CLARITY','PRICE','COLOR','POL','SYM','CUT','FLO_COL','DEPTH','TABLE','REMARK']
        if invobj:
           invobj.CRT=weight
           invobj.MESUREMNT=measurement
           invobj.CLARITY=clarity
           invobj.PRICE=price
           invobj.COLOR=color
           invobj.POL=polish
           invobj.SYM=symmetry
           invobj.CUT=cut
           invobj.FLO_COL=fluorescence
           invobj.DEPTH=depth
           invobj.TABLE=table
           invobj.REMARK=remarks
           invobj.UpdatedBy=user
           invobj.save()
           newobj=inventory.objects.filter(STK_ID=stk_id).first()
           diff=compare_objects(old_obj=prev,new_obj=newobj,allowkeys=allow)
           if len(diff)!=0:
            saveMessage("inventory",user,"Inventory",invobj.STK_ID,"Updated",user.get_username(),**{'changes':str(diff)})
           return HttpResponse(json.dumps({'message':'success'}))
        else:
           return HttpResponse(json.dumps({'message':'fail'}))
# def generate_qr_code(data):
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(data)
#     qr.make(fit=True)
#     qr_img = qr.make_image(fill_color="black", back_color="white")

#     # Save the QR code image
#     url = f"/media/qr/" + str(data) + ".png"
#     file_path = f"{BASE_DIR}{url}"
#     print(file_path)
#     qr_img.save(file_path)
#     return url


@login_required
def StockInfo(request):
    stocks = inventory.objects.all()
    context = {"stocks": stocks}
    return render(request, "inventory/all_details.html", context)


@login_required
def DiamondInfo(request):
    if request.method == "GET":
        q = request.GET["q"]
        info = inventory.objects.get(Scan_Id=q)
        pics = Video.objects.get(id_inv=info.Id)
        context = {"info": info, "pics": pics}
        return render(request, "inventory/diamond_details.html", context=context)


def generate_text(sid, weight, shape, color, purity):
    width, height = 200, 150
    background_color = (255, 255, 255)
    img1 = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(img1)
    text_color = (0, 0, 0)
    font_size = 15
    if len(shape) > 20:
        s = shape
        shape = f"""{s[:int(len(s)/2)]}
              {s[int(len(s)/2):]}"""

    text = f"""SID : {sid}
Weight: {weight}
Shape: {shape}
Colour: {color}
Purity: {purity}
    """
    font_path = "static/fonts/Roboto-Medium.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(text, font=font)
    x = (width - text_width) // 50
    y = (height - text_height) // 6
    draw.text((x, y), text, font=font, fill=text_color)
    return img1


def generate_footer(width, gia):
    text = f"""SAILAM .LTD               GIA: {gia}"""
    width, height = width, 10
    background_color = (255, 255, 255)
    footer = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(footer)
    text_color = (0, 0, 0)
    font_size = 9
    font_path = "static/fonts/Roboto-Medium.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(text, font=font)
    x = (width - text_width) // 5
    y = (height - text_height) // 2
    draw.text((x, y), text, font=font, fill=text_color)
    return footer


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"http://127.0.0.1:8000/inventory/diamond?q={data}")
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    url = f"/media/qr/" + str(data) + ".png"
    file_path = f"{BASE_DIR}{url}"
    qr_image.save(file_path)
    img2 = Image.open(file_path)
    return img2, file_path, url


def generate_sticker(data, sid, weight, shape, color, purity, gia):
    image1, file_path, url = generate_qr_code(data)
    image2 = generate_text(sid, weight, shape, color, purity)
    print(image1.height)
    last_height = int(image1.height / 3)
    height = last_height + 10
    image1 = image1.resize((int(image1.width * height / image1.height), height))
    image2 = image2.resize((int(image2.width * height / image2.height), height))
    width = image1.width + image2.width
    footer = generate_footer(width, gia)
    merged_image = Image.new("RGB", (width, height))
    merged_image.paste(image1, (0, 0))
    merged_image.paste(image2, (image1.width, 0))
    merged_image.paste(footer, (0, last_height))
    # print(merged_image.height, merged_image.width)
    merged_image.save(file_path)
    return url


def encrypt(data):
    return data <<19


def decrypt(data):
   return data>>19

@login_required
def scanner(request):
    groupdata=Tally.objects.all()
    result=[{'group':group.Name} for group in groupdata]
    data=[i for i in {x['group']:x for x in result}.values()]
    groupData = json.dumps(data)
    return render(request,"inventory/scanner.html",{"groupdata":groupData})

@login_required
def getTallyData(request,tally_id,tally_type):
    if tally_type=="insert":
        data=inventory.objects.filter(Scan_Id=tally_id,InvoiceMade=False,IsHide=False,TallyMade=False).values()|inventory.objects.filter(GIA_NO=tally_id,InvoiceMade=False,IsHide=False,TallyMade=False).values()
        if data:
            result={
                'stk_id':data[0]["STK_ID"],
                'desc':'<b>color:</b>'+data[0]["COLOR"]+', <b>clarity:</b>'+data[0]["CLARITY"]+', <b>shape:</b>'+data[0]["SHAPE"],
                'weight':data[0]["CRT"],
                'remark':data[0]["REMARK"],
                'price':data[0]["PRICE"]
            }
            return HttpResponse(json.dumps(result, indent = 4))
        else :
            result={
                'stk_id':'null',
            }
            return HttpResponse(json.dumps(result, indent = 4))
    elif tally_type=="remove":
      data=inventory.objects.filter(Scan_Id=tally_id,TallyMade=True).values()|inventory.objects.filter(GIA_NO=tally_id,TallyMade=True).values()
      if data:
            result={
                'stk_id':data[0]["STK_ID"],
                'desc':'<b>color:</b>'+data[0]["COLOR"]+', <b>clarity:</b>'+data[0]["CLARITY"]+', <b>shape:</b>'+data[0]["SHAPE"],
                'weight':data[0]["CRT"],
                'remark':data[0]["REMARK"],
                'price':data[0]["PRICE"]
            }
            return HttpResponse(json.dumps(result, indent = 4))
      else :
            result={
                'stk_id':'null',
            }
            return HttpResponse(json.dumps(result, indent = 4))
      

@login_required
def setTally(request,tally_type):
   if request.method=="POST":
      user=request.user
      data=json.loads(request.body)
      if tally_type=='insert':
        donew=data['new']
        group=data['group']
        stk=data['stk_id']
        if donew:
            tally=Tally.objects.create(Name=group,CretedBy=user)
            for id in stk:
                inv=inventory.objects.filter(STK_ID=id).last()
                TallyData.objects.create(stk_no=inv,tally_no=tally)
                inv.TallyMade=True
                inv.save()
        else:
            tally=Tally.objects.filter(Name=group).last()
            if tally:
                for id in stk:
                    inv=inventory.objects.filter(STK_ID=id).last()
                    obj,created=TallyData.objects.get_or_create(stk_no=inv,tally_no=tally)
                    if not created:
                       obj.submitted=False
                       obj.save()
                    inv.TallyMade=True
                    inv.save()
            else:
                tally=Tally.objects.create(Name=group,CretedBy=user)
                for id in stk:
                    inv=inventory.objects.filter(STK_ID=id).last()
                    TallyData.objects.create(stk_no=inv,tally_no=tally)
                    inv.TallyMade=True
                    inv.save()
        return HttpResponse("Success") 
      else:
         stk=data['stk_id']
         for id in stk:
            inv=inventory.objects.filter(STK_ID=id).last()
            tallydata=TallyData.objects.filter(stk_no=inv,submitted=False).last()
            if tallydata:
                tallydata.submitted=True
                tallydata.save()
            inv.TallyMade=False
            inv.save()
         return HttpResponse("Success")

@login_required
def getTallyView(request):
    return render(request,'inventory/viewtally.html')


@login_required
def getTally(request):
    result=[]
    tallylist=Tally.objects.filter(Isdeleted=False).order_by('-CreatedOn').values()
    # print(tallylist)
    for tally in tallylist:
       tallydic={}
       tallydic['name']=tally['Name']
       user=User.objects.filter(id=tally["CretedBy_id"]).first()
       tallydic['createdby']=str(user.first_name)+" "+str(user.last_name)
       tallydic['createdon']=datetime.datetime.strptime(str(tally['CreatedOn']), '%Y-%m-%d %H:%M:%S.%f%z')
       tallydata=TallyData.objects.filter(tally_no=tally['Id']).values()
       total=0
       pending=0
       tallydic['child_data']=[]
       for data in tallydata:
          total+=1
          tallychild={}
          inv=inventory.objects.filter(STK_ID=data['stk_no_id']).first()
          tallychild['stk_id']=inv.STK_ID
          tallychild['desc']='<b>color:</b>'+inv.COLOR+',<b> clarity:</b>'+inv.CLARITY+', <b>shape:</b>'+inv.SHAPE
          tallychild['weight']=inv.CRT
          tallychild['price']=inv.PRICE
          if not data['submitted']:
             pending+=1
          tallychild['status']=data['submitted']
          tallydic['child_data'].append(tallychild)
          tallydic['total']=total
          tallydic['pending']=pending
       result.append(tallydic)
    # print(result)
    return JsonResponse(result, safe=False)


@login_required
def getMemoData(request,scanid):
   data=inventory.objects.filter(Scan_Id=scanid,MemoMade=False,InvoiceMade=False,IsHide=False).values()|inventory.objects.filter(GIA_NO=scanid,MemoMade=False,InvoiceMade=False,IsHide=False).values()
   if data:
    result={
        'stk_id':data[0]["STK_ID"],
        'desc':'<b>color:</b>'+data[0]["COLOR"]+',<b> clarity:</b>'+data[0]["CLARITY"]+', <b>shape:</b>'+data[0]["SHAPE"],
        'weight':data[0]["CRT"],
        'remark':data[0]["REMARK"],
        'price':data[0]["PRICE"]
    }
    # print(result)
    return HttpResponse(json.dumps(result, indent = 4)) 
   else :
      result={
         'stk_id':'null',
      }
      return HttpResponse(json.dumps(result, indent = 4))
   
@login_required
def setMemoData(request):
    if request.method=="POST":
        user=request.user
        data=json.loads(request.body)
        client_name=data['client']['name']
        client_company=data['client']['company']
        client_address=data['client']['address']
        dohide=data['client']['dohide']

        _client=Client.objects.filter(name=client_name,company=client_company).first()
        if not _client:
         client=Client.objects.create(name=client_name,company=client_company,address=client_address)
         _client=client
        memo=Memo.objects.create(client=_client,CretedBy=user)
        for row in data['diamond']:
          stk_id=row['stk_no']
          description=row['description']
          weight=row['weight']
          remark=row['remark']
          rate=row['rate']
          inv=inventory.objects.filter(STK_ID=stk_id).first()
          inv.MemoMade=True
          if dohide:
             inv.IsHide=True
          inv.save()
          memodata=MemoData.objects.create(memo=memo,stk_no=inv,desc=description,weight=weight,rate=rate,remark=remark)
        if memodata:
         saveMessage("memo",user,"Memo",client_name,client_company,"memo","prepared",user.get_username(),"Having MemoId "+str(memo.id_memo))
         response=gen_report(request,data,memo)
         return response
        else:
         return HttpResponse("Error")
      


def gen_report(request,data,memo):
    file_name="memo_"+str(memo.id_memo)+".pdf"
    url = f'/media/pdf/'+file_name
    file_path = f'{BASE_DIR}{url}'
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []
    custom_style = ParagraphStyle(
    'CustomStyle',
    parent=getSampleStyleSheet()['Normal'],
    fontSize=8,
     )
    image_path = os.path.join(BASE_DIR, 'static', 'image', 'logo.png')
    logo = Img(image_path, width=0.9*inch, height=0.9*inch)
    elements.append(logo)
    # Header
    header_text = '<font size="10">APPROVAL MEMO</font>'
    header_style = getSampleStyleSheet()["Heading1"]
    header_style.alignment = 1
    header = Paragraph(header_text,header_style)
    elements.append(header)
    elements.append(Spacer(1, 10))
    
    # Company details
    company_details = [
        '<b><font size="15">SAILAM LIMITED</font></b>',
        "ROOM 1721, BEVERELY COMMERCIAL CENTER,",
        "87 CHATHAM ROAD SOUTH, TSIM SHA SUI HONGKONG",
        "<b>TELEPHONE :</b> 852-24241425 , 852-24241427",
        "<b>Wechat ID: </b>sailamsam",
        "<b>Mobile :</b> 852 9122 4906",
        "<b>email:</b> sailamltdhk@gmail.com",
        "<b>RAP NET ID</b> : 89199",
    ]

    company_style = getSampleStyleSheet()["Normal"]

    client_details=[
       "<b>Memo No:</b> "+str(memo.id_memo),
       "<b>Date: </b>"+str(memo.CreatedOn).split(" ")[0],
       "<b>To: </b>",
       "<b>Name: </b>"+data['client']['name'],
       "<b>Company:</b> "+data['client']['company'],
       "<b>Address: </b>"+data['client']['address'],
    ]
    
    
    client = [Paragraph(line, custom_style) for line in client_details]
    company= [Paragraph(line, custom_style) for line in company_details]
    data_company = [[para] for para in company]
    data_client= [[para] for para in client]

    table_style = [
        ("FONTSIZE", (0, 1), (-1, -1), 5), 
    ]
    company_table=Table(data_company,style=table_style)
    client_table=Table(data_client,style=table_style) 
    empty=[[" "],[" "],[" "],[" "],[" "],[" "]]
    empty_table=Table(empty)
    parent_table_data = [[company_table,empty_table, client_table]]
    parent_table = Table(parent_table_data,colWidths=[200,150,200])
    parent_table_style = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  
    ])
    parent_table.setStyle(parent_table_style)
    elements.append(parent_table)
    elements.append(Spacer(1, 10))

    inst_text="The goods described and valued as below are delivered to you for examinations and  inspection and inspection only and remain our property subject to ourorder and shall returned to SAILAM LIMTED on demand. Such merchandise until returned to us and actually recieved,are at you risk from all hazards. No right or power is given to you to sell, pledge, hypothecate or otherwise dispose of this merchandise regardless of prior transaction. A sale of this merchandise can only be effected and title will pass only if, as and when we the said owner shall agree to such sale and a  bill of sale rendered therefor."
    instruction = Paragraph(inst_text,custom_style)
    elements.append(instruction)
    elements.append(Spacer(1, 10))
    # Table
    table_data = [
        [Paragraph("LOT NO.", custom_style), Paragraph("DESCRIPTION", custom_style),Paragraph("CARATS", custom_style) ,Paragraph("Rate per Crt HK$/US$", custom_style) ,Paragraph("PENDING", custom_style) , Paragraph("RETURN", custom_style), Paragraph("CARATS SOLD", custom_style), Paragraph("REMARK", custom_style), Paragraph("CRT", custom_style)]
    ]
    
    for item in data['diamond']:
        table_data.append([
            Paragraph(item.get("stk_no", ""), custom_style),
            Paragraph(item.get("description", ""), custom_style),
            Paragraph(str(item.get("weight", "")), custom_style),
            Paragraph(str(item.get("rate", "")), custom_style),
            Paragraph("", custom_style),
            Paragraph("", custom_style),
            Paragraph("", custom_style),
            Paragraph(item.get("remark", ""), custom_style),
            Paragraph("", custom_style)
        ])
    colWidth=(0.4*inch,2.0*inch,0.4*inch,0.7*inch,0.7*inch,0.7*inch,0.7*inch,1.3*inch,0.7*inch)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1), 'TRUE'),  
    ])
    
    table = Table(table_data,colWidths=colWidth)
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 5))
    
    # Footer
    footer_text = "Received the above goods in good order on the terms and conditions set out (This is not an invoice or bill of sale). Duration of consignment is max. 7 days from the memo date"
    footer = Paragraph(footer_text, custom_style)
    elements.append(footer)
    elements.append(Spacer(1, 5))
    # Salesman 
    salesman_text = "<b>Salesman: </b>"+request.user.first_name
    salesman = Paragraph(salesman_text, custom_style)
    elements.append(salesman)
    elements.append(Spacer(1, 5))
    text1="<b>Time:</b> "+str(datetime.datetime.now().time().strftime("%H:%M:%S"))
    text2="<b>Chop & Signature______________</b>"
    text3="           "
    paragraph1 = Paragraph(text1, custom_style)
    paragraph2 = Paragraph(text2, custom_style)
    paragraph3 = Paragraph(text3, custom_style)
    story = [[paragraph1,paragraph3,paragraph2]]
    signtable=Table(story)
    elements.append(signtable)
    doc.build(elements)
    response = HttpResponse(file_name)
    return response


def send_pdf_response(request, file_name):
    url = f'/media/pdf/'+file_name
    file_path = f'{BASE_DIR}{url}'
    print(file_path)
    if os.path.exists(file_path):
        f = open(file_path, "rb")
        response = FileResponse(f, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(file_name)
        return response
    else:
        return HttpResponse("File not found.")
    

def preparedMemo(request):
   memoobj=Memo.objects.filter(is_deleted=False).values()
   result=[]
   stri=""
   for row in memoobj:
      memo={}
      memo['memo_id']=row['id_memo']
      memo['date']=str(row['CreatedOn'].date())
      client_id=row['client_id']
      client=Client.objects.filter(id_client=client_id).values()
      memo['client_name']=client[0]['name']
      memo['client_company']=client[0]['company']
      memo_data=MemoData.objects.filter(memo=row['id_memo']).values()
      memo['child_data']=[]
      for data in memo_data:
         child_memo={}  
         child_memo['stk_no']=data['stk_no_id']
         child_memo['description']=data['desc']
         child_memo['weight']=data['weight']
         child_memo['rate']=data['rate']
         child_memo['remarks']=data['remark']
         memo["child_data"].append(child_memo)
      result.append(memo)
   return HttpResponse(json.dumps(result, indent = 4))

@login_required
def viewMemo(request):
   return render(request,'inventory/memo.html')

@login_required
def viewHidden(request):
   return render(request,'inventory/viewhide.html')

@login_required
def deleteMemo(request,memo_id):
   user=request.user
   memo=Memo.objects.filter(id_memo=memo_id).first()
   memodata=MemoData.objects.filter(memo=memo_id).values()
   if memo:
      current_time=datetime.datetime.now(tz=datetime.timezone.utc)
      for row in memodata:
         stk_no=row['stk_no_id']
         inv=inventory.objects.filter(STK_ID=stk_no).first()
         inv.MemoMade=False
         inv.save()
      memo.is_deleted=True
      memo.DeletedBy=user
      memo.DeletedOn=current_time
      memo.save()
      client=memo.client
      saveMessage("memo",user,"Memo",client.name,client.company,"memo","deleted",user.get_username(),"Having MemoId "+str(memo.id_memo))

      return HttpResponse(json.dumps({'message':'success'}))
   else:
      return HttpResponse(json.dumps({'message':'fail'}))


def getinvoicedata(request,scanid):
   data=inventory.objects.filter(Scan_Id=scanid,InvoiceMade=False,IsHide=False).values()|inventory.objects.filter(GIA_NO=scanid,InvoiceMade=False,IsHide=False).values()
   if data:
    result={}
    result={
        'NO':data[0]["STK_ID"],
        'DESCRIPTION':'color:'+data[0]["COLOR"]+', clarity:'+data[0]["CLARITY"]+', shape:'+data[0]["SHAPE"],
        'PCS':1,
        'CTS':data[0]["CRT"],
        'CFR_US_$':data[0]["PRICE"]
    }
    # print(result)
    return HttpResponse(json.dumps(result, indent = 4)) 
   else :
      result={
         'NO':'null',
      }
      return HttpResponse(json.dumps(result, indent = 4))
   
@login_required
def setInvoiceData(request):
    if request.method=="POST":
        user=request.user
        data=json.loads(request.body)
        client_name=data['client']['name']
        client_company=data['client']['company']
        client_address=data['client']['address']
        _client=Client.objects.filter(name=client_name,company=client_company).first()
        if not _client:
        #  print("inside create")
         client=Client.objects.create(name=client_name,company=client_company,address=client_address)
         _client=client
        invoice=Invoice.objects.create(client=_client,CretedBy=user)
        if invoice:
           saveMessage("memo",user,"Invoice",client_name,client_company,"invoice","prepared",user.get_username(),"Having InvoiceId "+str(invoice.id_invoice))
        for row in data['diamond']:
          stk_id=row['stk_no']
          description=row['description']
          pcs=row['pcs']
          weight=row['weight']
          cfr=row['cfr']
          total=row['total']
          inv=inventory.objects.filter(STK_ID=stk_id).first()
          if inv:
            inv.InvoiceMade=True
            inv.save()
          InvoiceData.objects.create(invoice=invoice,stk_no=inv,desc=description,pcs=pcs,weight=weight,cfr=cfr,total=total)
        response=gen_invoice(request,data,invoice)
        return response

def gen_invoice(request,data,invoice):
    file_name="invoice_"+str(invoice.id_invoice)+".pdf"
    url = f'/media/pdf/'+file_name
    file_path = f'{BASE_DIR}{url}'
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []
    custom_style = ParagraphStyle(
    'CustomStyle',
    parent=getSampleStyleSheet()['Normal'],
    fontSize=8,
     )
    custom_style2 = ParagraphStyle(
    'CustomStyle',
    parent=getSampleStyleSheet()['Normal'],
    fontSize=6,
     )
    image_path = os.path.join(BASE_DIR, 'static', 'image', 'logo.png')
    logo = Img(image_path, width=0.9*inch, height=0.9*inch)
    elements.append(logo)
    # Header
    header_text = '<font size="10">Invoice</font>'
    header_style = getSampleStyleSheet()["Heading1"]
    header_style.alignment = 1
    header = Paragraph(header_text, header_style)
    elements.append(header)
    elements.append(Spacer(1, 3))
    
    # Company details
    company_details = [
        '<font size="15">SAILAM LIMITED</font>',
        "ROOM 1721, BEVERELY COMMERCIAL CENTER,",
        "87 CHATHAM ROAD SOUTH, TSIM SHA SUI HONGKONG",
        "<b>TELEPHONE :</b> 852-24241425 , 852-24241427",
        "<b>Mobile :</b> 852 9122 4906",
        "<b>email:</b> sailamltdhk@gmail.com",
    ]

    company_style = getSampleStyleSheet()["Normal"]

    client_details=[
       "<b><u>Sold To</u></b> ",
       "<b>M/S.</b> "+data['client']['name'],
       "<b>Company:</b> "+data['client']['company'],
       "<b>Address: </b>"+data['client']['address'],
    ]

    invoice_details=[
       "<b>INVOICE NO: </b>"+str(invoice.id_invoice),
       "<b>TERMS :</b>",
       "<b>DATE  :</b>"+str(datetime.datetime.now().date()),
    ]
    client = [Paragraph(line, custom_style) for line in client_details]
    company= [Paragraph(line, custom_style) for line in company_details]
    invoice= [Paragraph(line, custom_style) for line in invoice_details]
    data_company = [[para] for para in company]
    data_client= [[para] for para in client]
    data_inv=[[para] for para in invoice]
    table_style = [
        ("FONTSIZE", (0, 1), (-1, -1), 5), 
    ]
    company_table=Table(data_company,style=table_style)
    client_table=Table(data_client,style=table_style) 
    invoice_table=Table(data_inv,style=table_style)
    elements.append(company_table)
    elements.append(Spacer(1, 3))
    
    parent_table_data = [[client_table,invoice_table]]
    parent_table = Table(parent_table_data)
    elements.append(parent_table)
    elements.append(Spacer(1, 3))
    
    # Table
    table_data = [
        [Paragraph("LOT NO.", custom_style), Paragraph("DESCRIPTION", custom_style),Paragraph("PCS", custom_style) ,Paragraph("CTS", custom_style) ,Paragraph("CFR US $", custom_style) , Paragraph("TOTAL US$", custom_style)]
    ]
    pcs=0
    cts=0.0
    cfr=0.0
    total=0.0
    for item in data['diamond']:
        pcs+=int(item.get("pcs"))
        cts+=float(item.get("weight"))
        cfr+=float(item.get("cfr"))
        total+=(float(item.get("weight"))*float(item.get("cfr")))
        table_data.append([
            Paragraph(item.get("stk_no", ""), custom_style),
            Paragraph(item.get("description", ""), custom_style),
            Paragraph(str(item.get("pcs", "")), custom_style),
            Paragraph(str(item.get("weight", "")), custom_style),
            Paragraph(str(item.get("cfr", "")),custom_style),
            Paragraph(str(item.get("total", "")), custom_style)
        ])
    table_data.append([
            Paragraph(" ", custom_style),
            Paragraph("<b>Total</b>", custom_style),
            Paragraph(str(pcs), custom_style),
            Paragraph(str(cts), custom_style),
            Paragraph(str(cfr), custom_style),
            Paragraph(str(total), custom_style)
        ])
    colWidth=(0.5*inch,2.4*inch,0.7*inch,0.7*inch,0.9*inch,0.9*inch)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1), 'TRUE'),  
    ])
    
    table = Table(table_data,colWidths=colWidth)
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 3))
    
    footer_text = "<b>"+num2words(int(total)).upper()+" ONLY"+"</b>"
    footer = Paragraph(footer_text, custom_style2)
    elements.append(footer)
    elements.append(Spacer(1, 2))
    custom_stylepara = ParagraphStyle(
    'CustomStyle',
    parent=getSampleStyleSheet()['Normal'],
    fontSize=6,
    backColor=colors.beige 
)
    table1_data ="PAYMENT INSTRUCTION<br/>1 DIRECT PAYMENTS<br/>Send Crossed chq. Made payable 'Sailam Limited' indicate our Invoice number behind the chq.<br/>2 Direct Transfers to Bank Account<br/>Bank's Name : HSBC<br/>Name of Bank Account : SAILAM LTD.<br/>A/C NO: 817-016124-838<br/>Swift Code : HSBCHKKHHHKH<br/>When making remittance please ensure you indicate whom the funds are from and our invoice no to enable us identify them<br/>Over due date payment will be charged 2% per month"
    table2_data = "DECLARATION<br/>The Diamonds here in Invoiced have been purchased from legitimate sources not involved in funding conflict diamonds and in compliance with United Nation- Resolutions.The seller hereby guarantees conflict diamonds and in compliance with United Nation- Resolutions.The seller hereby guarantees provided by the supplier of these diamonds.<br/>TERMS OF PAYMENT_____________________<br/>PAYMENT DUE DATE: ___________________<br/>CHEQUE NO: __________________________<br/>CASH : ____________________________"
    text3="           "
    paragraph1 = Paragraph(table1_data, custom_stylepara)
    paragraph2 = Paragraph(table2_data, custom_stylepara)
    paragraph3 = Paragraph(text3, custom_style2)
    story = [[paragraph1,paragraph3,paragraph2]]
    main_table = Table(story)
    main_table_style = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  
    ])
    main_table.setStyle(main_table_style)
    elements.append(main_table)
    elements.append(Spacer(1, 1))

    text1="<b>SOLD GOOD ARE NOT REFUNDABLE</b><br/><b>CONFIRMED BY:</b><br/>CHOP & BUYERS SIGNATURE<br/>PHONE NO :_________________________"
    text2="<b>for SAILAM LIMITED</b><br/>CHOP & AUTHORIZED SIGN<br/>TIME:"+str(datetime.datetime.now().time().strftime("%H:%M:%S"))
    text3="           "
    
    paragraph1 = Paragraph(text1, custom_style2)
    paragraph2 = Paragraph(text2, custom_style2)
    paragraph3 = Paragraph(text3, custom_style2)
    story = [[paragraph1,paragraph3,paragraph2]]
    signtable=Table(story)
    elements.append(signtable)
    doc.build(elements)
    
    response = HttpResponse(file_name)
    return response


def getHideData(request,scanid):
   data=inventory.objects.filter(Scan_Id=scanid,InvoiceMade=False,IsHide=False).values()|inventory.objects.filter(GIA_NO=scanid,InvoiceMade=False,IsHide=False).values()
   if data:
    result={
        'stk_id':data[0]["STK_ID"],
        'desc':'color:'+data[0]["COLOR"]+', clarity:'+data[0]["CLARITY"]+', shape:'+data[0]["SHAPE"],
        'weight':data[0]["CRT"],
        'remark':data[0]["REMARK"],
        'price':data[0]["PRICE"]
    }
    # print(result)
    return HttpResponse(json.dumps(result, indent = 4)) 
   else :
      result={
         'stk_id':'null',
      }
      return HttpResponse(json.dumps(result, indent = 4))

@login_required
def setHideData(request):
   if request.method=="POST":
      data=json.loads(request.body)
      for id in data['stk_id']:
         inv=inventory.objects.filter(STK_ID=id).first()
         if inv:
            inv.UpdatedBy=request.user
            inv.IsHide=True
            inv.save()

   return HttpResponse("Success")


def getHideStock(request):
   result=[]
   hideobj=inventory.objects.filter(IsHide=True).values()
   
   for row in hideobj:
      hide={}
      hide['stk_id']=row['STK_ID']
      hide['weight']=row['CRT']
      hide['measurement']=row['MESUREMNT']
      hide['clarity']=row['CLARITY']
      hide['price']=row['PRICE']
      hide['child_data']=[]
      child={}
      child['color']=row['COLOR']
      child['polish']=row['POL']
      child['symmetry']=row['SYM']
      child['cut']=row['CUT']
      child['fluorescence']=row['FLO_COL']
      child['depth']=row['DEPTH']
      child['table']=row['TABLE']
      child['remarks']=row['REMARK']
      hide['child_data'].append(child)
      result.append(hide)
   return HttpResponse(json.dumps(result, indent = 4))

@login_required
def showDiamond(request,stk_id):
   user=request.user
   current_time=datetime.datetime.now(tz=datetime.timezone.utc)
   inv=inventory.objects.filter(STK_ID=stk_id).first()
   if inv:
      inv.IsHide=False
      inv.UpdatedBy=user
      inv.UpdatedOn=current_time
      inv.save()
      return HttpResponse(json.dumps({'message':'success'}))
   else:
    return HttpResponse(json.dumps({'message':'fail'}))

@login_required   
def allView(request):
   return render(request,'inventory/viewallstock.html')

@login_required
def getAll(request):
   result=[]
   hideobj=inventory.objects.filter().values()
   
   for row in hideobj:
      hide={}
      hide['stk_id']=row['STK_ID']
      hide['weight']=row['CRT']
      hide['measurement']=row['MESUREMNT']
      hide['clarity']=row['CLARITY']
      hide['price']=row['PRICE']
      hide['child_data']=[]
      if row['InvoiceMade']:
         hide['status']='Sold'
         inv=InvoiceData.objects.filter(stk_no=row['STK_ID']).last()
         hide['inv_id']=inv.invoice.id_invoice
      elif row['MemoMade']:
         hide['status']="Memo Prepared"
      elif row['IsHide']:
         hide['status']='Hidden'
      else:
         hide['status']='Available'
        
      child={}
      child['color']=row['COLOR']
      child['polish']=row['POL']
      child['symmetry']=row['SYM']
      child['cut']=row['CUT']
      child['fluorescence']=row['FLO_COL']
      child['depth']=row['DEPTH']
      child['table']=row['TABLE']
      child['remarks']=row['REMARK']
      hide['child_data'].append(child)
      result.append(hide)
   return HttpResponse(json.dumps(result, indent = 4))
