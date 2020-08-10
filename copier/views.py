from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import Company, Copier, DriverFile
from .forms import CopierForm
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def copier_update(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    copier = Copier.objects.get(id=pk)
    if request.method == 'POST':
        copier_form = CopierForm(request.POST, instance=copier)
        if copier_form.is_valid():
            copier_form.save(True)
            return redirect('copier:list')
    copier_form = CopierForm(instance=copier)
    html = render_to_string('copier_update_form.html', context={'form': copier_form, 'instance': copier}, request=request)
    return HttpResponse(html)


@login_required
def copier_upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        if files:
            DriverFile.objects.bulk_create(DriverFile(file=file) for file in files)
    return redirect('copier:list')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def copier_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    copier_list = Copier.objects.all()
    page = request.GET.get('page', 1)
    if request.method == 'POST':
        copier_form = CopierForm(request.POST)
        if copier_form.is_valid():
            copier_form.save(commit=True)
            return redirect('copier:list')
    else:
        copier_form = CopierForm()
    paginator = Paginator(copier_list, 10)
    try:
        copiers = paginator.page(page)
    except PageNotAnInteger:
        copiers = paginator.page(1)
    except EmptyPage:
        copiers = paginator.page(paginator.num_pages)

    return render(request, 'copier_list.html', {
        'form': copier_form,
        'copier_list': copiers
    })
