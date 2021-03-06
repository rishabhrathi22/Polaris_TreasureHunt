from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('solve/', views.solve),
    path('leaderboard/', views.leaderboard),
    path('hint/', views.get_hint)
]
