from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post, UserExtended


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    if request.method == "POST":
        content = request.POST["post_content"]
        post = Post(post=content, user=request.user)
        post.save()
        return redirect('index')
    return render(request, 'network/new_post.html')

def all_posts(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, "network/all_posts.html", {"posts": posts})

def profile(request, username):
    user = User.objects.get(username=username)
    user_extended, created = UserExtended.objects.get_or_create(user=user)
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    followers = user_extended.followers.count()
    following = UserExtended.objects.filter(followers=user).count()
    is_following = request.user in user_extended.followers.all()

    context = {
        'user_profile': user,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_following': is_following
    }
    return render(request, 'network/profile.html', context)


def following(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    # Access the 'following' attribute from the User model
    following_users = request.user.userextended.followers.all()
    posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')

    return render(request, "network/following.html", {"posts": posts})

