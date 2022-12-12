from django.urls import path
from .views import index
from . import views

app_name='oands'
urlpatterns = [
    path('', index, name='index'),
]
