from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CommandExecution",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("command", models.CharField(max_length=100)),
                ("args", models.TextField(blank=True)),
                ("output", models.TextField(blank=True)),
                ("task_id", models.CharField(blank=True, max_length=255)),
                ("status", models.CharField(default="PENDING", max_length=20)),
                ("pid", models.IntegerField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
