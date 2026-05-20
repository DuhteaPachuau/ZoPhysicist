from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("lessons/<slug:slug>/", views.lesson_detail, name="lesson_detail"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),
    path("practice/", views.practice_home, name="practice_home"),
    path("practice/<str:exam>/", views.practice_exam, name="practice_exam"),
    path("practice/question/<int:pk>/", views.practice_question_detail, name="practice_question_detail"),
    path("lab/", views.lab_home, name="lab_home"),
    path("lab/waves/", views.lab_waves, name="lab_waves"),
    path("lab/pendulum/", views.lab_pendulum, name="lab_pendulum"),
    path("lab/lens/", views.lab_lens, name="lab_lens"),
    path("lab/spectrum/", views.lab_spectrum, name="lab_spectrum"),
    path("search/", views.search, name="search"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
