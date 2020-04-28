from parsing.models import Board
import django_filters

class BoardFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Board
        exclude = ['created', 'updated']