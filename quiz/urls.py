from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing),
    path('home', views.index),
    path('riddle', views.riddle),
    path('hint', views.hint),

    
]