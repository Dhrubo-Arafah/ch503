from django.shortcuts import render, redirect

from community.forms import CommunityCreationForm, MakeRequestForm, CommunityUpdateForm
from community.models import Community, MakeRequest


def community(request):
    communities = Community.objects.all()
    context = {
        'communities': communities
    }
    return render(request, 'community/communities.html', context)


def create_group(request):
    form = CommunityCreationForm()
    if request.method == "POST":
        form = CommunityCreationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'community/create.html', context)


def update_community(request, id):
    community = Community.objects.get(id=id)
    form = CommunityUpdateForm(instance=community)
    if request.method == "POST":
        form = CommunityUpdateForm(request.POST, request.FILES, instance=community)
        if form.is_valid():
            form.save()
            return redirect("community", id=id)
    context = {'form': form}
    return render(request, 'community/update.html', context)


def make_request(request, id):
    form = MakeRequestForm(request.user)
    if request.method == "POST":
        form = MakeRequestForm(request.user, request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.community = Community.objects.get(id=id)
            data.save()
            return redirect('communities')
    context = {
        'form': form
    }
    return render(request, 'community/request.html', context)


def my_community(request):
    communities = Community.objects.filter(creator=request.user)
    context = {
        'communities': communities
    }
    return render(request, 'community/communities.html', context)


def single_community(request, id):
    community = Community.objects.get(id=id)
    requests = MakeRequest.objects.filter(community_id=id)
    print(community)
    context = {
        'community': community,
        'requests': requests
    }
    return render(request, 'community/community.html', context)
