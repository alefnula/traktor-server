from datetime import datetime, timedelta

from django.db import models
from django.db.models import Q
from tea import timestamp as ts
from tea_console.config import TeaConsoleConfig

from traktor.models.task import Task
from traktor.models.entry import Entry


config = TeaConsoleConfig.get_application_config()


class HistoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("task", "task__project")


class History(models.Model):
    timestamp = models.DateTimeField(null=False, blank=False)
    task = models.ForeignKey(
        Task, null=False, blank=False, on_delete=models.CASCADE
    )
    cumulative_duration = models.BigIntegerField(
        default=0, null=False, blank=False
    )
    yearly_duration = models.IntegerField(default=0, null=False, blank=False)
    monthly_duration = models.IntegerField(default=0, null=False, blank=False)
    weekly_duration = models.IntegerField(default=0, null=True, blank=True)

    objects = HistoryManager()

    class Meta:
        app_label = "traktor_server"
        ordering = ["-timestamp"]

    @property
    def cumulative_time(self) -> str:
        return ts.humanize(self.cumulative_duration)

    @property
    def yearly_time(self) -> str:
        return ts.humanize(self.yearly_duration)

    @property
    def monthly_time(self) -> str:
        return ts.humanize(self.monthly_duration)

    @property
    def weekly_time(self) -> str:
        return ts.humanize(self.weekly_duration)

    @classmethod
    def create(cls, task: Task):
        this_ts = ts.now()
        start_of_year = ts.make_aware(
            datetime(this_ts.year, 1, 1), config.timezone
        )
        start_of_month = ts.make_aware(
            datetime(this_ts.year, this_ts.month, 1), config.timezone
        )
        start_of_week = this_ts - timedelta(days=this_ts.weekday())

        last = cls.objects.filter(task=task).order_by("-timestamp").first()
        if last is None:
            last_ts = ts.make_aware(datetime(2000, 1, 1), config.timezone)
            cumulative_duration = 0
            yearly_duration = 0
            monthly_duration = 0
            weekly_duration = 0
        else:
            last_ts = last.timestamp
            cumulative_duration = last.cumulative_duration
            if last_ts.year == this_ts.year:
                yearly_duration = last.yearly_duration
            else:
                yearly_duration = 0

            if last_ts.year == this_ts.year and last_ts.month == this_ts.month:
                monthly_duration = last.monthly_duration
            else:
                monthly_duration = 0

            if (this_ts - last_ts).days < 7 and (
                last_ts.weekday() <= this_ts.weekday()
            ):
                weekly_duration = last.weekly_duration
            else:
                weekly_duration = 0

        entries = Entry.objects.filter(
            Q(task=task) & (Q(end_time__isnull=True) | Q(end_time__gt=last_ts))
        )
        for entry in entries:
            # Cumulative
            start = max(last_ts, entry.start_time)
            if entry.end_time is None:
                cumulative_duration += (this_ts - start).total_seconds()
            else:
                cumulative_duration += (entry.end_time - start).total_seconds()

            # Yearly
            start = max(last_ts, entry.start_time, start_of_year)
            if entry.end_time is None:
                yearly_duration += (this_ts - start).total_seconds()
            else:
                if entry.end_time < start_of_year:
                    continue
                yearly_duration += (entry.end_time - start).total_seconds()

            # Monthly
            start = max(last_ts, entry.start_time, start_of_month)
            if entry.end_time is None:
                monthly_duration += (this_ts - start).total_seconds()
            else:
                if entry.end_time < start_of_month:
                    continue
                monthly_duration += (entry.end_time - start).total_seconds()

            # Weekly
            start = max(last_ts, entry.start_time, start_of_week)
            if entry.end_time is None:
                weekly_duration += (this_ts - start).total_seconds()
            else:
                if entry.end_time < start_of_week:
                    continue
                weekly_duration += (entry.end_time - start).total_seconds()

        return cls.objects.create(
            timestamp=this_ts,
            task=task,
            cumulative_duration=int(cumulative_duration),
            yearly_duration=int(yearly_duration),
            monthly_duration=int(monthly_duration),
            weekly_duration=int(weekly_duration),
        )
