from django.urls import path
from . import views

urlpatterns = [
    path('hot', views.index, name="hot"),
    path('tag/<str:title>', views.tag, name="tag"),
    path('questions/question<int:i>', views.question, name="question"),
    path('login', views.login, name="login"),
    path('registration', views.signup, name="registration"),
    path('ask', views.ask, name="ask"),
]
