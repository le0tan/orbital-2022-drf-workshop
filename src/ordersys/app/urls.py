from django.urls import path

from . import views

urlpatterns = [
    # `name` arg is optional, but helpful for `reverse()` function
    # ref: https://docs.djangoproject.com/en/4.0/topics/http/urls/#naming-url-patterns
    path('', views.index, name='index'),
]
