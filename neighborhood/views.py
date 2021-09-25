from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile,Neighborhood,Business,Post
from rest_framework.views import APIView
from .forms import UpdateUserForm, ProfileForm, NeighborHoodForm, BusinessForm, PostForm

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
    pass

@login_required(login_url='/accounts/login/')
def single_hood(request):
    pass

def join(request):
    pass

def leave(request):
    pass

@login_required(login_url='/accounts/login/')
def search_profile(request):
    pass

class ProfileList(APIView):
    pass

class UserList(APIView):
    pass
