from . import views
from django.urls import path

urlpatterns = [
    path('user/', views.logged_User.as_view(), name='logged-in-user'),  #get
    
    path('user/register',views.Registerview.as_view(),name="register"), #post
    path('user/login',views.Loginview.as_view(),name="login"),          #post
    path('user/logout',views.Logoutview.as_view(),name="logout"),       #post
    
    path('user/post',views.postview.as_view(),name="user_post"),    #get , post (user post)
    path("post/like/<str:post_id>",views.Postlikeview.as_view(),name="postlikeview"), #get, post, delete
    path("post/comment/<str:post_id>",views.Postcommentview.as_view(),name="postcommentview"), #get, post, put, delete
    
    
    path('user/u/<str:username>',views.Userview.as_view(),name="user_view"), #get
    path('user/u/<str:username>/post',views.Userviewposts.as_view(),name="user_view_posts"), #get
]