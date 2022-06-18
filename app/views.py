from urllib import request

from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Question, Answer, Profile, Tag
from .forms import LoginForm, SignUpForm, EditProfile

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


def login_view(request):
    if request.method == 'GET':
        user_form = LoginForm()
    elif request.method == 'POST':
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = authenticate(request, **user_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return redirect(reverse('login'))

    return render(request, "login.html", {"form": user_form})

# @login_required()

def signup(request):
    if request.method == 'GET':
        user_form = SignUpForm()
    elif request.method == 'POST':
        user_form = EditProfile(data=request.POST)
        if user_form.is_valid():
            return render(request, "registration.html", {"form": user_form})


def logout_view(request):
    logout(request)

    # TODO: redirect текущую страницу
    return redirect(reverse("index"))


def index(request):
    return render(request, "index.html", make_content(Question.objects.all().values(), request))


@login_required(redirect_field_name="login")
def profile(request):
    return render(request, "profile.html")


@login_required(redirect_field_name="login")
def profile_edit(request):
    if request.method == 'GET':
        user_form = EditProfile()
    elif request.method == 'POST':
        user_form = EditProfile(data=request.POST)

    return render(request, "profile_edit.html", {"form": user_form})

# @login_required(redirect_field_name='login')
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

