from urllib import request
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

QUESTIONS = [
    {
        "title": f"title {i}",
        "text": f"This is test for qustion #{i}",
        "img": "./img/no_war.jpeg"
    } for i in range(5)
]

TAGS = [f"name {i}" for i in range(50)]

def index(request):
    return render(request, "index.html", {"questions" : QUESTIONS})

def ask(request):
    return render(request, "ask.html")