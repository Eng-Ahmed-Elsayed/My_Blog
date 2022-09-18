from django.urls import path
from . import views


urlpatterns = [
    path('recent/', views.recent_posts, name='recent'),
    path('trending/', views.trending_posts, name='trending'),
    path('create/', views.create_post, name='create_post'),
    path('<int:pk>/update/', views.update_post, name='create_post'),
    path('<int:pk>/', views.post_details, name='post_details'),

]