import cv2
from django.shortcuts import redirect, render

def index(request):

    return render(request, "dashboard.html")

def scanner(request):
    return render(request,"scanner.html")
