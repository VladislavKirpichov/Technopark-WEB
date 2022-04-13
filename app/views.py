from urllib import request
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.generic import ListView


# Create your views here.

PAGINATION_SIZE = 10

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque tempor id risus vel facilisis. Nunc commodo non orci a mattis. Fusce nulla erat, mollis non ipsum ac, finibus accumsan ligula. Nam et nulla eget neque consequat imperdiet. Ut pharetra odio aliquam lacinia lacinia. Curabitur non dui sed est finibus tempor nec vitae dui. Donec fermentum leo arcu, nec finibus mi pretium nec. Proin finibus semper purus vel convallis. Quisque eget fermentum dui. Morbi sollicitudin sit amet odio eget dignissim. Curabitur nec nisi hendrerit neque rhoncus egestas at quis tellus. Pellentesque quam sem, elementum eu sapien a, iaculis cursus lectus. Etiam ut nulla vel est ultricies fringilla. Maecenas pretium ultricies nibh, efficitur cursus ante volutpat sit amet. "

QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i + 1}",
        "hot": True,
        "tags": [f"hello", f"tag{i}"],
        "text": f"This is test for qustion #{i}\n" + LOREM_IPSUM,
        "img": "/img/img.jpg"
    } for i in range(25)
]

ANSWERS = [
    {
        "id": i,
        "user": "Vladislav Kirpichov",
        "content": LOREM_IPSUM,
        "questionId": i,
        "img": "./img/no_war.jpeg"
    } for i in range(25)
]

TAGS = [f"tag {i}" for i in range(50)]


def paginator(objects_list, request, per_page=20):
    pages = Paginator(objects_list, PAGINATION_SIZE)
    page_number = request.GET.get('page')
    page = pages.get_page(page_number)

    return pages, page


def index(request):
    pages, page = paginator(QUESTIONS, request, PAGINATION_SIZE)
    content = {
        "paginator": pages,
        "page_content": page,
    }
    return render(request, "index.html", {"paginator": pages, "page_content": page})


def ask(request):
    return render(request, "ask.html")


def question(request, i: int):
    content = {
        "question": QUESTIONS[i],
        "answers": [answer for answer in ANSWERS if QUESTIONS[i]["id"] == answer["questionId"]]
    }
    return render(request, "question_page.html", content)


def tag(request, tag: str):
    pages, page = paginator([qstn for qstn in QUESTIONS if tag in qstn["tags"]], request, PAGINATION_SIZE)
    content = {
        "paginator": pages,
        "page_content": page, "tag": tag
    }
    return render(request, "questions_by_tag.html", content)


def hot(request):
    pages, page = paginator(QUESTIONS[:25], request, PAGINATION_SIZE)
    content = {
        "paginator": pages,
        "page_content": page, "tag": tag
    }
    return render(request, "index.html", content)


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "registration.html")

