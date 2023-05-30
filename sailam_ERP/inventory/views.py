from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import requests
import json
from django.conf import settings
from .models import inventory
from .forms import VideoForm
import qrcode
import os
from io import BytesIO

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
                request.POST["link"] = did
                # print(request.POST)
                form = VideoForm(request.POST, request.FILES)
                if form.is_valid():
                    #    saving video and image to media
                    video = form.save(commit=False)
                    video.id_inv = stock
                    video.save()
                    form = VideoForm()
                    #    generating qr code
                    path = generate_qr_code(scan)
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
    url = f"/media/qr/" + str(data) + ".png"
    file_path = f"{BASE_DIR}{url}"
    print(file_path)
    qr_img.save(file_path)
    return url


def encrypt(data):
    return data << 19


def decrypt(data):
    return data >> 19
