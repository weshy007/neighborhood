from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile,Neighborhood,Business,Post
from rest_framework.views import APIView

# Create your views here.
def index(request):
    pass

@login_required(login_url='/accounts/login/')
def profile(request):
    pass

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
