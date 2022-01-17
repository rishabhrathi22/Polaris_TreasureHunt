from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing),
    path('home', views.home),
    path('solve', views.solve),
    path('leaderboard', views.leaderboard)
]