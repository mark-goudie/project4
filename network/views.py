from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, UserExtended

import json


def index(request):
    posts_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts_list, 10)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, "network/index.html", {"posts": posts})


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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    elif request.method == "POST":
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
    posts_list = Post.objects.filter(user=user).order_by('-timestamp')
    paginator = Paginator(posts_list, 10)  # Show 10 posts per page

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

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

    user_extended, created = UserExtended.objects.get_or_create(user=request.user)
    following_users = user_extended.following.all()

    # Debugging: Print the usernames of followed users
    print("Following Users:", [user.username for user in following_users])

    posts_list = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    
    # Debugging: Check if any posts are returned
    print("Number of Posts:", posts_list.count())

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, "network/following.html", {"posts": posts})




def all_posts(request):
    posts_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts_list, 10)  # Show 10 posts per page

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, "network/all_posts.html", {"posts": posts})

@login_required
@csrf_exempt
def update_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id, user=request.user)
        data = json.loads(request.body)
        post.content = data['content']
        post.save()
        return JsonResponse({"message": "Post updated successfully."}, status=200)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found or not authorized to edit."}, status=404)

from django.http import JsonResponse

def like_post(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    try:
        post = Post.objects.get(pk=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({"likes": post.likes.count(), "liked": liked})
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

@login_required
def toggle_follow(request, username):
    if request.method == "POST":
        target_user = User.objects.get(username=username)
        user_extended, created = UserExtended.objects.get_or_create(user=request.user)

        if target_user in user_extended.following.all():
            user_extended.following.remove(target_user)
        else:
            user_extended.following.add(target_user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
