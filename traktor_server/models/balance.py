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
        return (
            super()
            .get_queryset()
            .select_related("task", "task__project", "task__project__user")
        )


class Balance(models.Model):
    timestamp = models.DateTimeField(null=False, blank=False)
    task = models.OneToOneField(
        Task, null=False, blank=False, on_delete=models.CASCADE, unique=True
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

        balance = cls.objects.filter(task=task).first()
        if balance is None:
            last_ts = ts.make_aware(datetime(2000, 1, 1), config.timezone)
            balance = cls.objects.create(timestamp=this_ts, task=task)
        else:
            last_ts = balance.timestamp
            balance.timestamp = this_ts
            if last_ts.year != this_ts.year:
                balance.yearly_duration = 0

            if last_ts.year != this_ts.year or last_ts.month != this_ts.month:
                balance.monthly_duration = 0

            if (this_ts - last_ts).days >= 7 or (
                last_ts.weekday() > this_ts.weekday()
            ):
                balance.weekly_duration = 0

        entries = Entry.objects.filter(
            Q(task=task) & (Q(end_time__isnull=True) | Q(end_time__gt=last_ts))
        )
        for entry in entries:
            # Cumulative
            start = max(last_ts, entry.start_time)
            if entry.end_time is None:
                balance.cumulative_duration += (
                    this_ts - start
                ).total_seconds()
            else:
                balance.cumulative_duration += (
                    entry.end_time - start
                ).total_seconds()

            # Yearly
            start = max(last_ts, entry.start_time, start_of_year)
            if entry.end_time is None:
                balance.yearly_duration += (this_ts - start).total_seconds()
            else:
                if entry.end_time < start_of_year:
                    continue
                balance.yearly_duration += (
                    entry.end_time - start
                ).total_seconds()

            # Monthly
            start = max(last_ts, entry.start_time, start_of_month)
            if entry.end_time is None:
                balance.monthly_duration += (this_ts - start).total_seconds()
            else:
                if entry.end_time < start_of_month:
                    continue
                balance.monthly_duration += (
                    entry.end_time - start
                ).total_seconds()

            # Weekly
            start = max(last_ts, entry.start_time, start_of_week)
            if entry.end_time is None:
                balance.weekly_duration += (this_ts - start).total_seconds()
            else:
                if entry.end_time < start_of_week:
                    continue
                balance.weekly_duration += (
                    entry.end_time - start
                ).total_seconds()

        balance.save()
        return balance
