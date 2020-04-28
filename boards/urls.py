from django.conf.urls import url

from . import views
from .filters import BoardFilter
from django_filters.views import FilterView

app_name = 'boards'

urlpatterns = [
    # url(r'^$', views.file_downloads, name='home'),
    url(r'^$', views.home, name='boards'),
    url(r'^search/$', FilterView.as_view(filterset_class=BoardFilter, template_name='board/home.html'), name='board-filter'),
]