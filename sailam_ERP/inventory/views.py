import io
import os
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import requests
import json
from django.conf import settings
from .models import inventory,Client,Memo,MemoData
from .models import inventory, Video
from .forms import VideoForm
from .constant import authorization,urlendpoint
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os
from io import BytesIO
import qrcode
from PIL import Image, ImageDraw, ImageFont

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

        response = requests.post(urlendpoint, data=json.dumps(query), headers=headers)
        data = response.json()
    return HttpResponse(json.dumps(data), content_type="application/json")


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
        scan = 0

        if inventory.objects.last() == None:
            scan = encrypt(1)
        else:
            scan = encrypt(inventory.objects.last().Id)
        print(scan)
        exist = inventory.objects.filter(GIA_NO=giano).values()
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
            )
            if stock:
                link = request.POST["link"]
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
        form = VideoForm()
        return render(request, "inventory/inventory.html", {"form": form})


def viewStock(request):
    stocks = inventory.objects.all()
    context = {"stocks": stocks}
    return render(request, "inventory/viewinventory.html", context)


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
    return data << 19


def decrypt(data):
   return data>>19

def scanner(request):
    return render(request,"inventory/scanner.html")

def getMemoData(request,scanid):
   data=inventory.objects.filter(Scan_Id=scanid,MemoMade=False).values()|inventory.objects.filter(GIA_NO=scanid,MemoMade=False).values()
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
    elements.append(Spacer(1, 20))
    
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
    
    parent_table_data = [[company_table, client_table]]
    parent_table = Table(parent_table_data,colWidths=[200,300])
    parent_table_style = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  
    ])
    parent_table.setStyle(parent_table_style)
    elements.append(parent_table)
    elements.append(Spacer(1, 20))

    inst_text="The goods described and valued as below are delivered to you for examinations and  inspection and inspection only and remain our property subject to ourorder and shall returned to SAILAM LIMTED on demand. Such merchandise until returned to us and actually recieved,are at you risk from all hazards. No right or power is given to you to sell, pledge, hypothecate or otherwise dispose of this merchandise regardless of prior transaction. A sale of this merchandise can only be effected and title will pass only if, as and when we the said owner shall agree to such sale and a  bill of sale rendered therefor."
    instruction = Paragraph(inst_text)
    elements.append(instruction)
    elements.append(Spacer(1, 20))
    # Table
    table_data = [
        ["LOT NO.", "DESCRIPTION", "CARATS", "Rate per Crt HK$/US$", "PENDING", "RETURN", "CARATS SOLD", "REMARK"]
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
    
    table = Table(table_data)
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Footer
    footer_text = "Received the above goods in good order on the terms and conditions set out (This is not an invoice or bill of sale). Duration of consignment is max. 7 days from the memo date"
    footer_style = getSampleStyleSheet()["Normal"]
    footer = Paragraph(footer_text, footer_style)
    elements.append(footer)
    elements.append(Spacer(1, 20))
    
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
