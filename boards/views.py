from django.shortcuts import render
from parsing.models import Board, StatusPrice
from django.core.paginator import Paginator
from .filters import BoardFilter
import datetime

# Create your views here.
def home(request):

    boards_all = Board.objects.prefetch_related('boards').all()
    boards_list = BoardFilter(request.GET, queryset=boards_all)
    current_month = datetime.date.today().month
    month_range = range(1, 13)
    page = request.GET.get('page', 1)
    paginator = Paginator(boards_list.qs, 20)

    try:
        boards = paginator.get_page(page)
    except PageNotAnInteger:
        boards = paginator.page(1)
    except EmptyPage:
        boards = paginator.page(paginator.num_pages)

    context_data = {
        # 'class_active': v.release.version == pkg.b.release.version and "active" or "inactive",
        # 'class_latest': v.release.version == project.latest.version and "latest" or "notlatest",
        'boards': boards,
        'current_month': current_month,
        'month_range': month_range
    }

    return render(request, 'boards/home.html', context_data)

