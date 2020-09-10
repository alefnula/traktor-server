# Generated by Django 3.1.1 on 2020-09-10 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("traktor", "0006_project_slug_unique_for_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="History",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField()),
                ("cumulative_duration", models.BigIntegerField(default=0)),
                ("yearly_duration", models.IntegerField(default=0)),
                ("monthly_duration", models.IntegerField(default=0)),
                (
                    "weekly_duration",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="traktor.task",
                    ),
                ),
            ],
            options={"ordering": ["-timestamp"]},
        ),
    ]