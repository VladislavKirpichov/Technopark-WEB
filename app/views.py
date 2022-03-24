from urllib import request
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

QUESTIONS = [
    {
        "title": f"title {i}",
        "text": f"This is test for qustion #{i}",
    } for i in range(5)
]

def index(request):
    return render(request, "index.html", {"questions": QUESTIONS})