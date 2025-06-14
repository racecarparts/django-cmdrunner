
from celery import shared_task
import subprocess
from .models import CommandExecution

@shared_task(bind=True)
def run_command(self, exec_id, command_name, *args):
    cmd_exec = CommandExecution.objects.get(id=exec_id)
    try:
        process = subprocess.Popen(
            ['python', 'manage.py', command_name, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        cmd_exec.pid = process.pid
        cmd_exec.save()

        for line in process.stdout:
            cmd_exec.output += line
            cmd_exec.save()

        process.wait()
        cmd_exec.status = 'SUCCESS' if process.returncode == 0 else 'FAILED'
        cmd_exec.save()
    except Exception as e:
        cmd_exec.output += f"\nERROR: {e}"
        cmd_exec.status = 'FAILED'
        cmd_exec.save()
