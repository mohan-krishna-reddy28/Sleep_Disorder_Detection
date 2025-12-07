from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('home/', views.home_page, name='home'),
    path('input/', views.input_page, name='input'),
    path('output/', views.predict_output, name='output'),
    path('about/', views.about_page, name='about'),
    path('logout/', views.logout_user, name="logout"),
]
