from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('get_options/',views.get_options, name="get_options"),
    path('get_chapters/',views.get_chapters, name="get_chapters"),
    path('get_chapter/',views.get_chapter, name="get_chapter"),
    path('got_correct/',views.got_correct, name="got_correct"),
    path('exercise/<str:answer>/', views.display_exercise, name="display_exercise")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
