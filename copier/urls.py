from django.urls import path
from django.urls import path, re_path
from . import views

app_name = "copier"
urlpatterns = [
    path('', view=views.copier_list, name='list'),
    path('upload/', view=views.copier_upload_files, name='upload'),
    path('update/<pk>/', view=views.copier_update, name='update'),
    path('scanner/<pk>/', view=views.company_update, name='scanner')
]
