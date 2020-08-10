from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth
from django.contrib.auth import views as auth_views, authenticate, login
from django.contrib.auth.models import User
from copier.models import Copier, Company
from django.http import HttpResponse, JsonResponse
from zipfile import ZipFile
from io import StringIO, BytesIO


def home(request):
    if request.user.is_authenticated:
        return redirect('settings')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                auth_views.auth_login(request, user)
                return redirect('home')
        # user = User.objects.get(pk=)
        # auth_views.auth_login(request, request.POST, backend='django.contrib.auth.backends.ModelBackend')
    form = AuthenticationForm(request)
    return render(request, 'home.html', {'form': form})


@login_required
def get_model_names(request):
    company = request.GET.get('company', '')
    color_mono = request.GET.get('color_mono', 1)
    bit = request.GET.get('bit', 1)
    copiers = Copier.objects.filter(color_mono=color_mono, bit=bit)
    if company:
        copiers = copiers.filter(company__id=company)
    model_names = list(copiers.values_list('model_name', flat=True))
    return JsonResponse({'model_names': model_names})


@login_required
def settings(request):
    user = request.user

    # try:
    #     kakao_login = user.social_auth.get(provider='kakao')
    # except UserSocialAuth.DoesNotExist:
    #     kakao_login = None
    #
    # can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
    # return render(request, 'settings.html', {
    #     'kakao_login': kakao_login,
    #     'can_disconnect': can_disconnect
    # })
    if user.is_superuser:
        return redirect('copier:list')
    if request.method == 'POST':

        model_name = request.POST.get('model_name', '')
        ip_address = request.POST.get('ip_address', '')
        copier = Copier.objects.filter(model_name=model_name).first()

        text = "{}\n".format(ip_address)
        text = "{}{}\n{}\n".format(text,
                                  "Color" if copier.color_mono == 1 else "Mono",
                                  "64bit" if copier.bit == 1 else "32bit")
        filename = 'download.txt'
        in_memory = BytesIO()
        zip = ZipFile(in_memory, 'a')
        zip.writestr('readme.txt', text)
        zip.write(copier.driver_file.file.path, copier.driver_file.file.name)
        for file in zip.filelist:
            file.create_system = 0
        zip.close()

        in_memory.seek(0)

        response = HttpResponse(in_memory, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=download.zip"
        # response.write(in_memory.read())

        # response = HttpResponse(text, content_type='text/plain')
        # response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response

    companies = Company.objects.all()
    model_list = []
    model_names = Copier.objects.filter(color_mono=1, bit=1).values_list('model_name', flat=True)

    if len(model_names) > 0:
        model_list = list(set(list(model_names)))
    return render(request, 'copier_search.html', {'company_list': companies, 'model_list': model_list})


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'password.html', {'form': form})


@login_required
def logout(request):
    auth_views.auth_logout(request)
    return redirect('home')
