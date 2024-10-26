from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path,include


router = DefaultRouter()
router.register(r'users', views.Users)


urlpatterns = [
    path('', include(router.urls)),
    path('user/', views.User.as_view(), name='logged-in-user'),
]