from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Post, Follower


def index(request):
    posts = Post.objects.all().order_by('-create_date')
    return render(request, "network/index.html", {
        'posts': [post.short() for post in posts]
    })


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


@login_required
def new_post(request):
    if request.method == 'POST':
        content = request.POST["new_content"]
        if len(content) > 0:
            try:
                post = Post(content= content, creator= request.user)
                post.save()
                print('new post added')
                return HttpResponseRedirect(reverse(index))
            except:
                return render(request, "network/index.html", {
                    "message": "Some thing went wrong"
                })
        else:
            return HttpResponseRedirect(request, "network/index.html", {
                "message": "you can't post nothing"
            })
    else:
        return render(request, "network/index.html", {
            "message": "it's not a POST request"
        })


def profile(request, username):
    info = User.objects.filter(username=username).first()
    posts = Post.objects.filter(creator=info.pk).order_by('-create_date')
    count_followers = len(info.followers.all())
    count_following = len(info.following.all())
    me = User.objects.filter(username= request.user.username)
    print(me)
    is_following = Follower.objects.filter(follower__in=me, following=info).exists()
    print(is_following)

    return render(request, 'network/profile.html', {
        'info': info,
        'posts': posts,
        'count_followers': count_followers,
        'count_following': count_following,
        'is_following': is_following
    })


@csrf_exempt
def follow(request):
    username = json.loads(request.body)['follow']
    crnt_user = User.objects.get(pk=request.user.id)
    follow = User.objects.get(username= username)
    follower = Follower.objects.filter(follower=crnt_user, following=follow)
    print('pass')
    if follower.exists():
        follower.delete()
        return JsonResponse({
            'message': 'error'
        })

    Follower.objects.create(follower=crnt_user, following=follow)
    return JsonResponse({
        'message': 'error'
    })


