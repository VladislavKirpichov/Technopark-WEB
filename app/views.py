from urllib import request
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.generic import ListView

from .models import Question, Answer, Profile, Tag


# Create your views here.

PAGINATION_SIZE = 10

# Tag.objects.add_new_tags()
# Profile.objects.add_new_profiles()
# Question.objects.add_new_questions()
# Answer.objects.add_new_answers()

def paginator(objects_list, per_page=20):
    objects = Paginator(objects_list, per_page)
    return objects


def index(request):
    pages = paginator(Question.objects.all().values(), PAGINATION_SIZE)
    page_number = request.GET.get('page')
    page = pages.get_page(page_number)
    return render(request, "index.html", {"paginator": pages, "page_content": page})


def ask(request):
    return render(request, "ask.html")


def question(request, i: int):
    qstn = Question.objects.get_question_by_id(i).values()
    answers = Paginator(Question.objects.get_question_answers(i).order_by('id').values(), PAGINATION_SIZE)
    return render(request, "question_page.html", {"question": qstn[0],
                                                  "answers": answers})


def tag(request, tag: str):
    pages = paginator(list(Question.objects.get_questions_by_tag(tag)), request, PAGINATION_SIZE)
    page_number = request.GET.get('page')
    page = pages.get_page(page_number)
    return render(request, "index.html", {"paginator": pages, "page_content": page})


def hot(request):
    return render(request, "index.html", {"page_content": list(Question.objects.get_hot())})


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "registration.html")

