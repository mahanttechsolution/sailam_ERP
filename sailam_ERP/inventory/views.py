import datetime
import io
import os
from django.shortcuts import render
from django.http import HttpResponse,FileResponse
import requests
import json
from django.conf import settings
from .models import inventory,Client,Memo,MemoData
from .forms import VideoForm
from .constant import authorization,urlendpoint
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

# Create your views here.

BASE_DIR = settings.BASE_DIR

def loadGiaData(request):
    if request.method=="POST":
        report_number = request.POST.get("gianumber")
        file1=open('static/query/master.txt')
        content=file1.read()
        query = {
        "query":content ,
        "variables": {
            "reportNumber": report_number
        }
        }

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": authorization
        }

        response = requests.post(urlendpoint, data=json.dumps(query), headers=headers)
        data = response.json()
    return HttpResponse(json.dumps(data),content_type="application/json")
    

def insertDiamond(request):
    if request.method=="POST":
       user=request.user
       stkid=request.POST.get("stkid")
       shape=request.POST.get("shape")
       color=request.POST.get("color")
       clarity=request.POST.get("clarity")
       polish=request.POST.get("polish")
       symmetry=request.POST.get("symmetry");
       cut=request.POST.get("cut")
       fluorescence=request.POST.get("fluorescence")
       mesurement=request.POST.get("mesurement")
       depth=request.POST.get("depth")
       table=request.POST.get("table")
       giano=request.POST.get("giano")
       remark=request.POST.get("remark")
       price=request.POST.get("price")
       crt=request.POST.get("crt")
       desc=request.POST.get("desc")
       scan=0
       if inventory.objects.last()==None:
        scan=encrypt(1)
       else:
        scan=encrypt(inventory.objects.last().Id+1)
       print(scan)
       exist=None
       print(giano)
       if not giano:
        exist=inventory.objects.filter(STK_ID=stkid).values()
       else:
        exist=inventory.objects.filter(GIA_NO=giano).values()
       if not exist:
        stock=inventory.objects.create(SHAPE=shape,COLOR=color,CLARITY=clarity,POL=polish,SYM=symmetry,CUT=cut,FLO_COL=fluorescence,MESUREMNT=mesurement,DEPTH=depth,TABLE=table,GIA_NO=giano,REMARK=remark,PRICE=price,STK_ID=stkid,CRT=crt,DESCRIPTION=desc,CretedBy=user,Scan_Id=scan)
        if stock:
          form = VideoForm(request.POST, request.FILES)
          if form.is_valid():
        #    saving video and image to media
           video = form.save(commit=False)
           video.id_inv=stock
           video.save()
           form=VideoForm() 
        #    generating qr code
           path=generate_qr_code(scan)
           return render(request,'inventory/inventory.html',{"message":"Data Inserted Successfully!","form":form,"qr_code_path":path})
          else:
           form=VideoForm() 
           return render(request,'inventory/inventory.html',{"errormessage":"Video and Photo is not uploaded","form":form})
       else:
          form=VideoForm()
          return render(request,'inventory/inventory.html',{"errormessage":"Data Is Already Present","form":form})
    else:
     form=VideoForm()
     return render(request,'inventory/inventory.html',{"form":form})
    

def viewStock(request):
    stocks=inventory.objects.all()
    context={
       "stocks":stocks
    }
    return render(request,'inventory/viewinventory.html',context)


def generate_qr_code(data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image
        url = f'/media/qr/'+str(data)+'.png'
        file_path = f'{BASE_DIR}{url}' 
        print(file_path)
        qr_img.save(file_path)
        return url

def encrypt(data):
   return data<<19

def decrypt(data):
   return data>>19

def scanner(request):
    return render(request,"inventory/scanner.html")

def getMemoData(request,scanid):
   data=inventory.objects.filter(Scan_Id=scanid,MemoMade=False,IsSold=False).values()|inventory.objects.filter(GIA_NO=scanid,MemoMade=False,IsSold=False).values()
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
   

def setMemoData(request):
    if request.method=="POST":
        user=request.user
        data=json.loads(request.body)
        client_name=data['client']['name']
        client_company=data['client']['company']
        client_address=data['client']['address']
        _client=Client.objects.filter(name=client_name,company=client_company).first()
        if not _client:
         print("inside create")
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
          inv.save()
          MemoData.objects.create(memo=memo,stk_no=inv,desc=description,weight=weight,rate=rate,remark=remark)
        response=gen_report(request,data,memo)
        return response
      

def gen_report(request,data,memo):
    file_name="memo_"+str(memo.id_memo)+".pdf"
    url = f'/media/memopdf/'+file_name
    file_path = f'{BASE_DIR}{url}'
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []
    
    # Header
    header_text = "APPROVAL MEMO"
    header_style = getSampleStyleSheet()["Heading1"]
    header_style.alignment = 1
    header = Paragraph(header_text, header_style)
    elements.append(header)
    elements.append(Spacer(1, 10))
    
    # Company details
    company_details = [
        "<b>SAILAM LIMITED</b>",
        "ROOM 1428, BEVERELY COMMERCIAL CENTER,",
        "87 CHATHAM ROAD SOUTH, TSIM SHA SUI HONGKONG",
        "<b>TELEPHONE :</b> 852-24241425 , 852-24241427",
        "<b>Wechat ID: </b>sailamsam",
        "<b>Mobile :</b> 852 9122 4906",
        "<b>email:</b> sailamltdhk@hotmail.com",
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
    
    styles = getSampleStyleSheet()
    paragraph_style = styles["Normal"]
    client = [Paragraph(line, paragraph_style) for line in client_details]
    company= [Paragraph(line, paragraph_style) for line in company_details]
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
    instruction = Paragraph(inst_text)
    elements.append(instruction)
    elements.append(Spacer(1, 10))
    # Table
    table_data = [
        [Paragraph("LOT NO.", company_style), Paragraph("DESCRIPTION", company_style),Paragraph("CARATS", company_style) ,Paragraph("Rate per Crt HK$/US$", company_style) ,Paragraph("PENDING", company_style) , Paragraph("RETURN", company_style), Paragraph("CARATS SOLD", company_style), Paragraph("REMARK", company_style)]
    ]
    
    for item in data['diamond']:
        table_data.append([
            Paragraph(item.get("stk_no", ""), company_style),
            Paragraph(item.get("description", ""), company_style),
            Paragraph(str(item.get("weight", "")), company_style),
            Paragraph(str(item.get("rate", "")), company_style),
            Paragraph("", company_style),
            Paragraph("", company_style),
            Paragraph("", company_style),
            Paragraph(item.get("remark", ""), company_style)
        ])
    colWidth=(0.9*inch,2.0*inch,0.9*inch,0.9*inch,0.9*inch,0.9*inch,0.9*inch,0.9*inch)
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
    elements.append(Spacer(1, 10))
    
    # Footer
    footer_text = "Received the above goods in good order on the terms and conditions set out (This is not an invoice or bill of sale). Duration of consignment is max. 7 days from the memo date"
    footer_style = getSampleStyleSheet()["Normal"]
    footer = Paragraph(footer_text, footer_style)
    elements.append(footer)
    elements.append(Spacer(1, 10))
    
    # Salesman 
    salesman_text = "<b>Salesman: </b>"+request.user.first_name
    salesman_style = getSampleStyleSheet()["Normal"]
    salesman = Paragraph(salesman_text, salesman_style)
    elements.append(salesman)
    doc.build(elements)

    response = HttpResponse(file_name)
    return response


def send_pdf_response(request, file_name):
    url = f'/media/memopdf/'+file_name
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

def viewMemo(request):
   return render(request,'inventory/memo.html')

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
      return HttpResponse(json.dumps({'message':'success'}))
   else:
      return HttpResponse(json.dumps({'message':'fail'}))
   
def getinvoicedata(request,scanid):
   data=inventory.objects.filter(Scan_Id=scanid,IsSold=False).values()|inventory.objects.filter(GIA_NO=scanid,MemoMade=False).values()
   if data:
    result={}
    result['data']={
        'NO':data[0]["STK_ID"],
        'DESCRIPTION':'color:'+data[0]["COLOR"]+', clarity:'+data[0]["CLARITY"]+', shape:'+data[0]["SHAPE"],
        'PCS':1,
        'CTS':data[0]["CRT"],
        'CFR US $':data[0]["PRICE"]
    }
    # print(result)
    return HttpResponse(json.dumps(result, indent = 4)) 
   else :
      result={
         'NO.':'null',
      }
      return HttpResponse(json.dumps(result, indent = 4))