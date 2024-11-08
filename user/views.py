from .forms import LoginForm, RegisterForm, UserProfileForm, UserForm
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import Profile, Follow
from django.contrib.auth.models import User
from django.http import Http404
from posts.models import Post
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
                
            else:
                messages.error(request, 'Invalid Credentials')
        else:
            messages.error(request, 'Error! Try Again')
    else:
        form  = LoginForm()
    return render(request, 'login.html', {'form':form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  

            login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, 'Error')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form':form})      

def logout_view(request):
    logout(request)
    return redirect('login')      

def profile_view(request):
    user_form = UserForm(instance=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    liked_posts = Post.objects.filter(like=request.user)  

    if request.method == 'POST':
        p_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        u_form = UserForm(request.POST, instance=request.user)
        
        if p_form.is_valid() and u_form.is_valid():
            user = u_form.save()
            profile = p_form.save(commit=False)
            profile.user = user  
            profile.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error Updating Profile! Check the form fields.')
    else:
        p_form = UserProfileForm(instance=profile)
        u_form = UserForm(instance=request.user)
    
    return render(request, 'profile.html', {
        'user_form': u_form,
        'profile_form': p_form,
        'liked_posts':liked_posts
    })

def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'user_list.html', {'users':users})

