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
    path('add-car/', views.add_car, name='add_car'),
    path('edit-car/<int:car_id>/', views.edit_car, name='edit_car'),
    path('toggle-user/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),
    path('update-booking/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]