from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth
from django.contrib.auth import views as auth_views, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from zipfile import ZipFile
from io import StringIO, BytesIO


def home(request):

    return render(request, 'home.html')


