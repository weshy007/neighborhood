from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import (BusinessForm, NeighborHoodForm, PostForm, ProfileForm,
                    UpdateUserForm)
from .models import Business, Neighborhood, Post, Profile
from .serializer import ProfileSerializer, UserSerializer


# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/accounts/login/')
def profile(request, username):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    parameters = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile.html', parameters)


@login_required(login_url='/accounts/login/')
def hoods(request):
    hoods = Neighborhood.objects.all()
    form = NeighborHoodForm(request.POST, request.FILES)
    print(form.errors)
    if form.is_valid():
        post = form.save(commit=False)
        post.admin = request.user.profile
        post.save()
        return redirect('hoods')
    else:
        form = NeighborHoodForm(request.POST, request.FILES)

    return render(request,'all_hoods.html',{"all_hoods":hoods,"form":form})

@login_required(login_url='/accounts/login/')
def single_hood(request, hood_id):
    hood = Neighborhood.objects.get(id=hood_id)
    business = Business.objects.filter(neighborhood=hood)
    posts = Post.objects.filter(hood=hood)
    posts = posts[::-1]
    if request.method == 'POST':
        form = BusinessForm(request.POST,request.FILES)
        if form.is_valid():
            bs_form = form.save(commit=False)
            bs_form.neighborhood = hood
            bs_form.user = request.user.profile
            bs_form.save()
            return redirect('single_hood', hood.id)
    else:
        form = BusinessForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.hood = hood
            post.user = request.user.profile
            post.save()
            return redirect('single_hood', hood.id)
    else:
        post_form = PostForm()
    parameters = {
        'hood': hood,
        'business': business,
        'post_form': post_form,
        'posts': posts,
        'form': form,
    }
    return render(request, 'single_hood.html', parameters)


def join(request):
    hood = get_object_or_404(Neighborhood, id=id)
    request.user.profile.neighborhood = hood
    request.user.profile.save()
    return redirect('single_hood', hood.id)


def leave(request):
    hood = get_object_or_404(Neighborhood, id=id)
    request.user.profile.neighborhood = None
    request.user.profile.save()
    return redirect('hoods')

@login_required(login_url='/accounts/login/')
def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = Business.search_business(name)
        print(results)
        message = f'name'

        return render(request, 'results.html', {'message': message, 'results': results})
    else:
        message = "You did not make any selection"

        return render(request, 'results.html', {'message': message})

class ProfileList(APIView):
     def get(self, request, format=None):
        all_profile = Profile.objects.all()
        serializers = ProfileSerializer(all_profile, many=True)
        return Response(serializers.data)

class UserList(APIView):
    def get(self, request, format=None):
        all_user = User.objects.all()
        serializers = UserSerializer(all_user, many=True)
        return Response(serializers.data)
