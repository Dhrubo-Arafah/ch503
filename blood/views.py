from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.models import Profile
from blood.forms import SeekingPost, ResponseForm
from blood.models import Post, Donation


@login_required(login_url='/accounts/login/')
def search(request):
    if request.method == "POST":
        location = request.POST['location']
        blood_group = request.POST['blood_group']

        if location == '':
            results = Profile.objects.filter(blood_group__icontains=blood_group)
        elif blood_group == '':
            results = Profile.objects.filter(location__icontains=location)
        else:
            results = Profile.objects.filter(blood_group__icontains=blood_group, location__icontains=location)
        context = {
            'search': f"{location} {blood_group}",
            'results': results
        }
        return render(request, 'blood/search_result.html', context)


def home(request):
    posts = Post.objects.filter(blood_managed=0)
    page = request.GET.get('page', 1)
    response_list = 0
    if request.user.is_authenticated:
        responded = Donation.objects.filter(donor=request.user)
        response_list = responded.values_list('post', flat=True)
        if request.method == 'POST' and request.user.is_authenticated:
            thana = request.POST["thana"]
            blood_group = request.POST["blood_group"]
            posts = Post.objects.filter(thana__icontains=thana, blood_group__icontains=blood_group, blood_managed=0)
    paginator = Paginator(posts, 3)
    try:
        all_posts = paginator.page(page)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = Paginator.page(paginator.num_pages)
    context = {
        'posts': all_posts,
        'response_list': response_list
    }
    return render(request, 'index.html', context)


@login_required(login_url='/accounts/login/')
def create_post(request):
    form = SeekingPost()
    if request.method == 'POST':
        form = SeekingPost(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            return redirect('index')
    context = {
        'form': form
    }
    return render(request, 'blood/create.html', context)


@login_required(login_url='/accounts/login/')
def update_post(request, id):
    form_data = Post.objects.get(id=id)
    form = SeekingPost(instance=form_data)
    if request.method == 'POST':
        form = SeekingPost(data=request.POST, instance=form_data)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
        'form': form
    }
    return render(request, 'blood/update.html', context)


@login_required(login_url='/accounts/login/')
def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return HttpResponseRedirect("/")


def view_post(request, id):
    post = Post.objects.get(id=id)
    context = {
        'post': post,
    }
    return render(request, 'blood/response.html', context)


@login_required(login_url='/accounts/login/')
def my_posts(request):
    posts = Post.objects.filter(user=request.user)
    context = {
        'posts': posts
    }
    return render(request, 'index.html', context)


@login_required(login_url='/accounts/login/')
def add_response(request, id):
    form = ResponseForm()
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.post_id = id
            form_data.donor = request.user
            form_data.save()
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form
    }
    return render(request, 'blood/response_form.html', context)


@login_required(login_url='/accounts/login/')
def remove_response(request, id):
    post = Post.objects.get(id=id)
    already_responsed = Donation.objects.filter(post=post, donor=request.user)
    already_responsed.delete()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/accounts/login/')
def show_responses(request, id):
    responses = Donation.objects.filter(post_id=id)
    total_bags = sum(responses.values_list('bags', flat=True))
    post = Post.objects.get(id=id)
    context = {
        'responses': responses,
        'post': post,
        'total_bags': total_bags
    }
    return render(request, 'blood/response.html', context)


@login_required(login_url='/accounts/login/')
def approve(request, r_id, pk):
    response = Donation.objects.get(id=r_id)
    if response.approve == 0:
        response.approve = 1
        response.save()
        return redirect('show_response', id=pk)
    else:
        response.approve = 0
        response.save()
        return redirect('show_response', id=pk)


@login_required(login_url='/accounts/login/')
def contributions(request):
    responses = Donation.objects.filter(donor=request.user, approve=1)
    context = {
        'responses': responses
    }
    return render(request, 'blood/contributions.html', context)


@login_required(login_url='/accounts/login/')
def cont_detail(request, id):
    response = Donation.objects.get(id=id)
    context = {
        'response': response
    }
    return render(request, 'blood/cont_detail.html', context)
