from django.urls import path 
from . import views

urlpatterns = [
    path('register',views.userRegisterView.as_view(),name='register'),
    path('login',views.userLoginView.as_view(),name='login'),
    path('profile',views.ProfileView.as_view(),name='profile'),
    path('changepass',views.ChangePassView.as_view(),name='change_pass'),
    path('send',views.SendEmailView.as_view(),name='send'),
    path('reset/<uid>/<token>',views.ResetPassView.as_view(),name='reset'),
]
