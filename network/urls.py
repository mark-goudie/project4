
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("all_posts", views.all_posts, name="all_posts"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("toggle_follow/<str:username>", views.toggle_follow, name="toggle_follow"),
    path("update_post/<int:post_id>", views.update_post, name="update_post"),
    path("like/<int:post_id>", views.like_post, name="like_post")
]
