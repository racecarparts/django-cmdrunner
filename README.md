# cmdrunner

Run Django management commands from the admin interface with live output and Celery task tracking.

## 🚀 Setup Instructions (Using GitHub URL in `requirements.txt`)

If you're installing `cmdrunner` via GitHub in your `requirements.txt`:

```
git+https://github.com/racecarparts/django-cmdrunner.git@[tag/release]
```

### 1. Add to `INSTALLED_APPS`

In `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'cmdrunner.apps.CmdrunnerConfig',
]
```

### 2. Run Migrations
```bash
python manage.py migrate cmdrunner
```

### 3. Confirm Celery is Running
Ensure your Celery worker is active:
```bash
celery -A yourproject worker -l info
```

### 4. Verify Admin UI
Visit `http://localhost:8000/admin/` and look for **Command Executions** under the **Cmdrunner** section.

---

## 🔐 Admin Registration Note

Make sure you explicitly register the model with the Django admin. Either use:

```python
@admin.register(CommandExecution)
class CommandExecutionAdmin(admin.ModelAdmin):
    ...
```

**or**, if you're not using decorators, you must add:

```python
admin.site.register(CommandExecution)
```
