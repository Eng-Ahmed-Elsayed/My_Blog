from django.urls import path
from . import views


urlpatterns = [
    path('', views.authors, name='authors'),
    path('<int:pk>/', views.author_profile, name='author_profile'),
]