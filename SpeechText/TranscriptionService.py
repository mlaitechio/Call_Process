import subprocess
import sys
import os
import django
import traceback

sys.path.append("/".join(os.getcwd().replace("\\", "/").split("/")[0:-1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ABC.settings')
django.setup()

from AbcApp.models import CurrentProcessLog, Analytic
from ABC.settings import BASE_DIR


def process_file_for_transcription():
    get_total_count = CurrentProcessLog.objects.all().count()
    if get_total_count == 0:
        Obj = CurrentProcessLog()
        Obj.process_id = 1
        Obj.save()
        get_request_id = Analytic.objects.get(id=1)
        req_id = get_request_id.request_id
        path = BASE_DIR.replace("\\", "/") + "/" + "SpeechText/"
        file_path_with_argument = "python {0}TranscribeService.py {1}".format(path, req_id)
        subprocess.Popen(file_path_with_argument, shell=False)
    else:
        last_id = CurrentProcessLog.objects.latest('id')
        check_transcription_status = Analytic.objects.get(id=last_id.process_id)
        print(check_transcription_status.transcription_status)
        if check_transcription_status.transcription_status == "Failed" or check_transcription_status.transcription_status == "Completed":
            try:
                Analytic.objects.get(id=last_id + 1)
                is_next_id_present = True
            except Exception as e:
                is_next_id_present = False
            if is_next_id_present:
                increase_id = last_id + 1
                last_id.process_id = increase_id
                last_id.save()
                if check_transcription_status.id == last_id.process_id + 1:
                    fine_nxt_req_id = Analytic.objects.get(id=last_id.process_id + 1)
                    req_id = fine_nxt_req_id.request_id
                    path = BASE_DIR.replace("\\", "/") + "/" + "SpeechText/"
                    file_path_with_argument = "python {0}TranscribeService.py {1}".format(path, req_id)
                    subprocess.Popen(file_path_with_argument, shell=False)
        elif check_transcription_status.transcription_status == "In Progress":
            return None
        elif check_transcription_status.transcription_status == "Not Started":
            last_id = CurrentProcessLog.objects.latest('id')
            check_transcription_status = Analytic.objects.get(id=last_id.process_id)
            req_id = check_transcription_status.request_id
            print(req_id)
            path = BASE_DIR.replace("\\", "/") + "/" + "SpeechText/"
            file_path_with_argument = "python {0}TranscribeService.py {1}".format(path, req_id)
            subprocess.Popen(file_path_with_argument, shell=False)

