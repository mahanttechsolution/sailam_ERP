import cv2
from django.shortcuts import redirect, render

def index(request):

    return render(request, "dashboard.html")

