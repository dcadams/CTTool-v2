from django.urls import path

from .views import index, convert_course

urlpatterns = [
    path('', index, name='index'),
    path('convert_course/', convert_course, name='index'),
]