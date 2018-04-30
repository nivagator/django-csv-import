import inspect, os
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils.encoding import smart_text, force_text
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.utils import timezone

# Create your views here.
from tablib import Dataset
from .resources import WarehouseResource
from .models import Warehouse

def home(request):
    return render(request, 'fileimport/home.html', {})

class ImportHistoryView(TemplateView):
    paginate_by = 25
    template_name = 'fileimport/history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug_list = list(set(Warehouse.objects.values_list('slug', flat=True)))
        slug_list.sort()
        context['slugs'] = slug_list
        return context

class ImportList(ListView):
    paginate_by = 25
    template_name = 'fileimport/validate.html'

    def get_queryset(self, *args, **kwargs):
        if self.kwargs:
            query = self.kwargs["slug"]
            qs = Warehouse.objects.filter(slug=query)
            # print(qs)
        else:
           qs = Warehouse.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs:
            context['page_title'] = 'Import Validation'
        else:
            context['page_title'] = 'Warehouse'
        return context

def download(request, path):
    # print(os.path.join(settings.BASE_DIR, os.path.join('media/', path)))
    file_path = os.path.join(settings.BASE_DIR, os.path.join('media/', path))
    # print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def simple_upload(request):
    context = {}
    template = 'fileimport/import.html'
    if request.method == 'POST':
        if not request.FILES:
            print('no file selected')
            template = 'fileimport/results.html'
            context = {
                "error": ['No file provided'],#['there','are','errors'],
            }
        else:
            slg = str(request.user) + "_" + timezone.now().strftime('%Y%m%d%H%M%S')
            person_resource = WarehouseResource()
            dataset = Dataset()
            new_persons = request.FILES['myfile']
            imported_data = dataset.load(force_text(new_persons.read()))
            result = person_resource.import_data(dataset, dry_run=True)  # Test the data import
            # print('dry run completed')
            if not result.has_errors():
                result = person_resource.import_data(dataset, dry_run=False)  # Actually import now
                a = result.rows
                b = []
                i = 0
                for id in a:
                    b.append(a[i].object_id)
                    i += 1
                Warehouse.objects.filter(pk__in=b).update(slug=slg)
                return HttpResponseRedirect(reverse('validate', kwargs={"slug":slg}))
            else:
                print('errors on import')
                template = 'fileimport/results.html'
                context = {
                    "error": ['error'],#['there','are','errors'],
                }
     
    return render(request, template, context)



