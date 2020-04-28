import time

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.views import View

from .forms import FileForm
from .models import *

import os
from .timezone_convert import convert_to_localtime
from datetime import date
from django.contrib.auth.models import User
from django.conf import settings
import importlib.util
import json
from django.views.decorators.http import condition
from .choices import STATUS_CHOICES
from .parsers.functions import operator_create, months_create
from django.template.loader import render_to_string
from django.core import serializers

# Create your views here.
# def file_downloads(request):
#     return render(request, 'parsing/file_download.html', locals())

class UploadView(View):
    def get(self, request):
        files_list = File.objects.order_by('-uploaded_at')
        return render(self.request, 'parsing/file_download.html', {'files': files_list})

    def post(self, request):
        time.sleep(1)
        # today = date.today()
        # today_files = File.objects.filter(uploaded_at__date=today)  
        form = FileForm(self.request.POST, self.request.FILES)
        username = str(User.objects.get(username=request.user))
        if form.is_valid():
            file = form.save(commit=False)
            file.title = os.path.basename(file.file.name)
            file.uploaded_by = request.user
            for key in import_dict:
                for value in import_dict[key]:
                    if value.lower() in os.path.basename(file.file.name).lower():
                        operator_id = operator_create(import_dict[key][0], key)
            file.operator_id = operator_id
            file.save()
            data = {'is_valid': True}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

import_dict = {
    'brok': ['Брок', 'brok', 'брок', 'бр_'],
    'prime': ['Прайм', 'prime', 'прайм'],
    # 'nasha_sprava': ['Наша справа'],
    'perehid': ['Перехід'],
    'raider': ['Рейдер', 'RAIDER'],
    'big_media': ['Біг медіа', 'Пономаренко'],
    'octagon': ['Октагон', 'Octagon'],
    'gal_contrakty': ['Галицькі контракти', 'Галицькі', 'Контракти', 'Гал.Контракти'],
    'svo': ['SV Outdoor', 'SVO', 'SV'],
    'media_mist': ['Медіа Міст', 'Міст'],
}

def get_file_list(request):
    if request.is_ajax():
        work_dir = os.path.join(settings.MEDIA_ROOT, 'workflow', str(date.today()))
        if os.path.exists(work_dir):
            base_file_list={}
            for filename in os.listdir(work_dir):
                files_from_db = File.objects.filter(file__contains=filename, uploaded_at__date=date.today(), status=1)
                for file in files_from_db:
                    base_file_list[filename] = file.id
            file_list = {value: key for key, value in base_file_list.items()}
            return HttpResponse(json.dumps(file_list), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'Error': 'Directory doesn\'t exists!'}), content_type='application/json')
    else:
        raise Http404

def refresh_table(request):
    files_list = File.objects.order_by('-uploaded_at').values('id', 'uploaded_at', 'file', 'status', 'uploaded_by__username', 'operator__name')
    for file in files_list:
        utcdate = convert_to_localtime("%d.%m.%Y, %H:%M:%S", file['uploaded_at'])
        file['uploaded_at'] = utcdate
        file['status'] = STATUS_CHOICES[file['status'] - 1][1]
        file['uploaded_by'] = file.pop('uploaded_by__username')
        file['operator'] = file.pop('operator__name')
    return JsonResponse({'result': list(files_list)})

