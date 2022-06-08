from django.shortcuts import render
from AbcApp.models import Analytic
from zipfile import ZipFile
#from AbcApp import transcription_start_cron
#from AbcApp.call_quality import qa_main
from ABC.settings import BASE_DIR
import os, csv
from django.http import JsonResponse
from django.http import HttpResponse
#views
def root(request):
    result = Analytic.objects.all().order_by('-id')
    #print(result)
    #qa = qa_main('/home/mayank/Documents/abc/speech/abcstt/media/1622758434405.txt')
    #transcription_start_cron.process_file_for_transcription()
    return render(request, 'dashboard.html', {"data": result})

def create_bulk_zip(request):
    if request.method == "GET":
        files = request.GET.getlist('files[]')
        media_path = os.path.join(BASE_DIR,'media')
        zipobj = ZipFile(media_path+'/bulk.zip','w')
        for file_name in files:
            zipobj.write(media_path+'/'+file_name+'.txt', os.path.basename(media_path+'/'+file_name+'.txt'))
        zipobj.close()
    return JsonResponse({'result':'success'})

def export_to_csv(request):
    model_class = Analytic

    meta = model_class._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=transcribed_report.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in model_class.objects.all():
        _ = writer.writerow([getattr(obj, field) for field in field_names])

    return response
