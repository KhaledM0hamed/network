
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("updatePost/", views.updatePost, name= "updatePost"),
    path("likePost/", views.likePost, name= "likePost"),
    path("unlikePost/", views.unlikePost, name= "unlikePost"),
]
