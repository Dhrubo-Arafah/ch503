from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from accounts.forms import CreateUserForm, LoginForm
from accounts.models import Profile
from accounts.forms import UpdateProfile, UpdateUser
from blood.models import Donation


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.last_login == None:
                    login(request, user)
                    return redirect(update_profile)
                else:
                    login(request, user)
                    return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


@login_required(login_url='/accounts/login/')
def logout_page(request):
    user = request.user.username
    logout(request)
    messages.success(request, user + ' Logged out Successfully')
    return redirect('/')


@login_required(login_url='/accounts/login/')
def profile(request, id):
    user = User.objects.get(id=id)
    try:
        response = Donation.objects.get(donor=user, approve=1)
    except:
        response = 0
    context = {
        'user': user,
        'response': response
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='/accounts/login/')
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UpdateUser(request.POST, instance=request.user)
        profile_form = UpdateProfile(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form = user_form.save()
            form = profile_form.save()
            messages.success(request, 'user profile has been updated')
            return redirect('/')
        else:
            messages.error(request, 'Form Submission Failed')
            return redirect('update_profile')
    else:
        user_form = UpdateUser(instance=request.user)
        profile_form = UpdateProfile(instance=profile)
        title = "Update Profile"
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'title': title
        }
        return render(request, 'accounts/update_profile.html', context)


@login_required(login_url='/accounts/login/')
def pass_change(request):
    current_user = request.user
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "your password has been updated")
            return redirect('profile')
    title = "Update Password"
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'accounts/password_update.html', context)


def delete_account(request):
    user = User.objects.get(username=request.user.username)
    user.delete()
    print(user)
    return redirect('index')
