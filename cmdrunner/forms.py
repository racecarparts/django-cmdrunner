from django import forms
from django.core.management import get_commands
from .models import CommandExecution


class CommandExecutionForm(forms.ModelForm):
    command = forms.ChoiceField(choices=[])

    class Meta:
        model = CommandExecution
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        command_choices = sorted(get_commands().keys())
        self.fields["command"].choices = [
            (cmd, cmd)
            for cmd in command_choices
            if cmd.startswith("yourapp") or cmd.startswith("custom")
        ]
