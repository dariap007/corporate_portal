from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('news/', views.news_list_view, name='news_list'),
    path('news/<int:news_id>/', views.news_detail_view, name='news_detail'),
    path('employees/', views.employees_list_view, name='employees_list'),
    path('employees/<int:employee_id>/', views.employee_detail_view, name='employee_detail'),
    path('documents/', views.documents_list_view, name='documents_list'),
    path('tickets/', views.tickets_list_view, name='tickets_list'),
    path('tickets/create/', views.ticket_create_view, name='ticket_create'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
]
