from . import views
from django.urls import path

urlpatterns = [
    path('user/', views.logged_User.as_view(), name='logged-in-user'),
    
]