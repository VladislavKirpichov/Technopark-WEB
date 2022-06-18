from django.urls import path
from . import views

urlpatterns = [
    path('hot', views.index, name="hot"),
    path('tag/<str:title>', views.tag, name="tag"),
    path('questions/question<int:i>', views.question, name="question"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup, name="signup"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.profile_edit, name="profile_edit"),
    path('logout/', views.logout_view, name="logout_view"),
    path('ask', views.ask, name="ask"),
    path('', views.index, name="index")
]