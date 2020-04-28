from django.conf.urls import url

from . import views

app_name = 'parsing'

urlpatterns = [
    url(r'^$', views.UploadView.as_view(), name='upload'),
    url(r'^ajax-get-list/', views.get_file_list, name='ajax-get-list'),
    url(r'^ajax-refresh-table/', views.refresh_table, name='ajax-refresh-table'),
]