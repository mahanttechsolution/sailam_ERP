from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import requests
import json
from django.conf import settings
from .models import inventory, Video
from .forms import VideoForm
import qrcode
import os
from io import BytesIO
import qrcode
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlretrieve
from django.core.paginator import Paginator

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
                ##image downloading
                try:
                    urlretrieve(
                        f"https://diamondvid.blob.core.windows.net/diamond-vid/www/viewer3/RealImages/{did}.jpg",
                        f"media/uploads/images/{did}.jpg",
                    )
                except Exception as e:
                    print("------------------------->", e)
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
    try:
        page_number = request.GET["page"]
    except:
        page_number = 1
    stocks = inventory.objects.all()

    p = Paginator(stocks, 10)
    page_obj = p.get_page(page_number)
    index = page_obj.number - 1

    if index >= 0:
        index = index * 10
    else:
        index = 0

    last_page = p.num_pages

    context = {"stocks": page_obj, "last_page": last_page}
    return render(request, "inventory/viewinventory.html", context)


def StockInfo(request):
    stocks = inventory.objects.all()
    context = {"stocks": stocks}
    return render(request, "inventory/all_details.html", context)


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
    return data >> 19
