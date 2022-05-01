from urllib import request
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.generic import ListView

from .models import Question, Answer, Profile, Tag


# Create your views here.

PAGINATION_SIZE = 10


def paginator(objects_list, request, per_page=20):
    pages = Paginator(objects_list, PAGINATION_SIZE)
    page_number = request.GET.get('page')
    page = pages.get_page(page_number)

    return pages, page

def make_content(objects_list, request, per_page=20):
    pages, page = paginator(objects_list, request, per_page)

    content = {
        "paginator": pages,
        "page_content": page,
        "tags": Tag.objects.all().values()[:20]
    }

    return content


def index(request):
    return render(request, "index.html", make_content(Question.objects.all().values(), request))


def ask(request):
    return render(request, "ask.html")


def question(request, i: int):
    try:
        qstn = Question.objects.get_question_by_id(i).values()
    except Question.DoesNotExist:
        return HttpResponseNotFound("<html><h1>404 Page Not Found:(</h1></html>")

    content = make_content(Question.objects.get_question_answers(i).values(), request)
    content["question"] = qstn[0]

    return render(request, "question_page.html", content)


def tag(request, title: str):
    # content = make_content(Tag.objects.get_questions_by_tag(title).values(), request)
    content = make_content(Question.objects.get_questions_by_tag_title(title).values(), request)
    return render(request, "index.html", content)


def hot(request):
    return render(request, "index.html", make_content(list(Question.objects.get_popular()), request))


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "registration.html")

