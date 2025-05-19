from django.urls import path
from . import views

app_name = 'rent'

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
]