from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns=[
    path('registraion/',views.UserCreationView.as_view(),name='registration'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/', login_required(views.UserLogOutView.as_view()),name='logout'),
    path('profile/', login_required(views.UserBankAccountUpdateView.as_view()),name='profile'),

]