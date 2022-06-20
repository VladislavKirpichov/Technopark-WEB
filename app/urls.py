from django.conf.urls.static import static
from django.urls import path

from askme import settings
from . import views

urlpatterns = [
    path('hot/', views.index, name="hot"),
    path('tag/<str:title>/', views.tag, name="tag"),
    path('questions/question<int:i>/', views.question, name="question"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup, name="signup"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.profile_edit, name="profile_edit"),
    path('logout/', views.logout_view, name="logout_view"),
    path('ask/', views.ask, name="ask"),
    path('answer/<int:id>/', views.answer, name="answer"),
    path('', views.index, name="index"),
    path('vote', views.vote, name="vote-view")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# TODO:
# static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)