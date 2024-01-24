from django.urls import path 
from . import views

urlpatterns = [
    path('register',views.userRegisterView.as_view(),name='register'),
    path('login',views.userLoginView.as_view(),name='login'),
]
