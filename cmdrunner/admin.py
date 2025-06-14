
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.utils.html import format_html
import os
import signal

from .models import CommandExecution
from .tasks import run_command

@admin.register(CommandExecution)
class CommandExecutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'command', 'status', 'pid', 'created', 'kill_link', 'retry_link')
    readonly_fields = ('command', 'args', 'output', 'status', 'task_id', 'pid', 'created')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/kill/', self.admin_site.admin_view(self.kill_command_view), name='kill_command'),
            path('<int:pk>/output/', self.admin_site.admin_view(self.command_output_view), name='command_output'),
            path('<int:pk>/retry/', self.admin_site.admin_view(self.retry_command_view), name='retry_command'),
        ]
        return custom_urls + urls

    def kill_link(self, obj):
        if obj.is_running():
            return format_html('<a class="button" href="{}">Kill</a>', f"{obj.id}/kill/")
        return "-"
    kill_link.short_description = 'Kill'

    def retry_link(self, obj):
        if obj.status in ('FAILED', 'KILLED'):
            return format_html('<a class="button" href="{}">Retry</a>', f"{obj.id}/retry/")
        return "-"
    retry_link.short_description = 'Retry'

    def kill_command_view(self, request, pk):
        obj = get_object_or_404(CommandExecution, pk=pk)
        if obj.pid:
            try:
                os.kill(obj.pid, signal.SIGTERM)
                obj.status = 'KILLED'
                obj.save()
                self.message_user(request, f"Process {obj.pid} killed.", messages.SUCCESS)
            except ProcessLookupError:
                obj.status = 'NOT FOUND'
                obj.save()
                self.message_user(request, f"PID {obj.pid} not found.", messages.WARNING)
        else:
            self.message_user(request, "No PID found.", messages.ERROR)
        return redirect(f'../../{pk}/change/')

    def command_output_view(self, request, pk):
        obj = get_object_or_404(CommandExecution, pk=pk)
        return HttpResponse(f"<pre style='white-space:pre-wrap'>{obj.output}</pre>")

    def retry_command_view(self, request, pk):
        obj = get_object_or_404(CommandExecution, pk=pk)
        args = obj.args.split()
        task = run_command.apply_async(args=[obj.id, obj.command] + args)
        obj.status = 'PENDING'
        obj.output = ''
        obj.task_id = task.id
        obj.pid = None
        obj.save()
        self.message_user(request, f"Command {obj.command} retried.", messages.INFO)
        return redirect(f'../../{pk}/change/')
