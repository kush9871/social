from django.shortcuts import redirect,render
# from . models import Profile,Post
from . models import *
from django.contrib import messages
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q


# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url
    if not request.user.is_authenticated:
        return redirect("Login")
    posts = Post.objects.filter(Q(profile__followers=request.user)& ~Q(likes=request.user))
    story = Story.objects.filter(profile__followers=request.user)
    context = {"posts":posts, "stories":story, 'profileimage':profileimage}
    return render(request,'index.html',context)


def createprofile(request):
    if request.user.is_authenticated:
        return redirect("profile") 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        image = request.FILES['image']
        user = User.objects.create_user(username=username,password=password)
        profile = Profile.objects.create(user = user, profile_picture = image)
        if profile:
            messages.success(request,'Profile Created Please Login')
            return redirect("Login")
    return render(request, 'signup.html')  

def Login(request):
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('profile')    
    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect("Login")

def profile(request,id=None):
    # if request.user.is_authenticated:
    #     return redirect("profile")
    if not request.user.is_authenticated:
        return redirect("Login")
    if id is not None:
        profile_id = Profile.objects.get(id=id)
        posts = Post.objects.filter(profile=profile_id)
        posts_num = posts.count()
        profile = Profile.objects.get(user=request.user)
        profileimage = profile.profile_picture.url
    else:
        profile_id = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(user=request.user)
        posts_num = posts.count()
        profile = Profile.objects.get(user=request.user)
        profileimage = profile.profile_picture.url
    return render(request,'profile.html',{'profile':profile_id,'profileimage':profileimage,'profile_of_user':True,'posts':posts,'posts_num':posts_num})

def search(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url
    search = request.GET['username']
    profiles = Profile.objects.filter(user__username__icontains=search)
    context = {'profiles':profiles,'username':search,"profileimage":profileimage}
    return render(request,'search.html',context)

def follow(request,id,username):
    profile = Profile.objects.get(id=id)
    Login_profile = Profile.objects.get(user=request.user)
    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
        Login_profile.followings.remove(profile.user)
    else:
        profile.followers.add(request.user)
        Login_profile.followings.add(profile.user)
    return redirect(f'/search?username={username}')

def upload_post(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url
    if request.method == 'POST':
        post = request.FILES['post']
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.create(user=request.user,image=post,profile=profile)
        if posts:
            messages.success(request,'Post Uploaded')
    return render(request, 'uploadpost.html',{'profileimage':profileimage})

def like_post(request,id):
    if not request.user.is_authenticated:
        return redirect("Login")
    post = Post.objects.filter(id = id)
    if request.user in post[0].likes.all():
        post[0].likes.remove(request.user)
    else:
        post[0].likes.add(request.user)
    return redirect('index')

def upload_reel(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url
    if request.method == 'POST':
        reel = request.FILES['reel']
        reels = Reels.objects.create(reel=reel)
        if reels:
            messages.success(request,'Reel Uploaded')
    return render(request, 'uploadreels.html',{'profileimage':profileimage})

def reels(request):
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url
    reels = Reels.objects.all()
    return render(request, 'reels.html',{'reels': reels, 'profileimage':profileimage})

def like_reel(request,id):
    reel = Reels.objects.get(id=id)
    if request.user in reel.likes.all():
        reel.likes.remove(request.user)
    else:
          reel.likes.add(request.user)
    return redirect("reels")

def upload_story(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url
    if request.method == 'POST':
        story = request.FILES['story']
        profile = Profile.objects.get(user=request.user)
        story_upload = Story.objects.create(story=story,profile=profile)
        if story_upload:
            messages.success(request,"STORY UPLOADED")
    return render(request,'uploadStory.html',{'profileimage':profileimage})
