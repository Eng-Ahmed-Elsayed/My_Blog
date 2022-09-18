from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('404/', views.error_page, name='404'),
    path('about_us/', views.about_us, name='about_us'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('search/', views.search, name='search'),
    

]