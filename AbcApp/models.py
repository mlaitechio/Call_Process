from django.db import models


class Analytic(models.Model):
    STATUS_CHOICES = (
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )
    request_id = models.CharField(max_length=500, blank=True, null=True)
    date_time = models.CharField(max_length=500, blank=True, null=True)
    campaign = models.CharField(max_length=500, blank=True, null=True)
    agent_name = models.CharField(max_length=500, blank=True, null=True)
    call_duration = models.CharField(max_length=500, blank=True, null=True)
    call_language = models.CharField(max_length=100, blank=True, null=True)
    call_status = models.CharField(max_length=500, blank=True, null=True)
    transcription_start_date_time = models.DateTimeField(blank=True, null=True)
    transcription_complete_date_time = models.DateTimeField(blank=True, null=True)
    json_blob_path = models.CharField(max_length=1000, blank=True, null=True)
    mp3_blob_path = models.CharField(max_length=1000, blank=True, null=True)
    transcribed_file = models.CharField(max_length=1000, blank=True, null=True)
    qa_score = models.CharField(max_length=500, blank=True, null=True)
    qa_color = models.CharField(max_length=500, blank=True, null=True)
    qa_escalation = models.CharField(max_length=500, blank=True, null=True)
    sentiment_score = models.CharField(max_length=500, blank=True, null=True)
    transcription_status = models.CharField(default=STATUS_CHOICES[0][0], max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.request_id


class CurrentProcessLog(models.Model):
    process_status = models.CharField(default="Stopped",max_length=500, null=True)
