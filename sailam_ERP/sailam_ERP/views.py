import cv2
from django.shortcuts import redirect, render


def scanner(request):
    return render(request,"scanner.html")
