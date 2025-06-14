
from django.db import models

class CommandExecution(models.Model):
    command = models.CharField(max_length=100)
    args = models.TextField(blank=True)
    output = models.TextField(blank=True)
    task_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default='PENDING')
    pid = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def is_running(self):
        return self.status in ('PENDING', 'STARTED') and self.pid
