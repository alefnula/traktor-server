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

    @staticmethod
    def __get_duration(
        entry: Entry, this_ts: datetime, start_time: datetime
    ) -> int:
        start_time = max(entry.start_time, start_time)

        if entry.end_time is None:
            return int((this_ts - start_time).total_seconds())
        else:
            return int((entry.end_time - start_time).total_seconds())

    @staticmethod
    def __bot():
        return ts.make_aware(datetime(2000, 1, 1), config.timezone)

    @classmethod
    def create(cls, task: Task, recalculate: bool = False):
        this_ts = ts.now()
        start_of_year = ts.make_aware(
            datetime(this_ts.year, 1, 1), config.timezone
        )
        start_of_month = ts.make_aware(
            datetime(this_ts.year, this_ts.month, 1), config.timezone
        )
        start_of_week = (this_ts - timedelta(days=this_ts.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        if recalculate:
            try:
                balance = cls.objects.get(task=task)
                balance.timestamp = this_ts
                balance.cumulative_duration = 0
                balance.yearly_duration = 0
                balance.monthly_duration = 0
                balance.weekly_duration = 0
            except cls.DoesNotExist:
                balance = cls.objects.create(timestamp=this_ts, task=task)
            last_ts = cls.__bot()
            entries = Entry.objects.filter(task=task)
        else:
            try:
                balance = cls.objects.get(task=task)
                last_ts = balance.timestamp
                balance.timestamp = this_ts
                if last_ts.year != this_ts.year:
                    balance.yearly_duration = 0

                if (
                    last_ts.year != this_ts.year
                    or last_ts.month != this_ts.month
                ):
                    balance.monthly_duration = 0

                if (this_ts - last_ts).days >= 7 or (
                    last_ts.weekday() > this_ts.weekday()
                ):
                    balance.weekly_duration = 0
            except cls.DoesNotExist:
                last_ts = cls.__bot()
                balance = cls.objects.create(timestamp=this_ts, task=task)

            entries = Entry.objects.filter(
                Q(task=task)
                & (Q(end_time__isnull=True) | Q(end_time__gt=last_ts))
            )

        for entry in entries:
            # Cumulative
            balance.cumulative_duration += cls.__get_duration(
                entry=entry, this_ts=this_ts, start_time=last_ts
            )

            # Yearly
            if entry.end_time is None or entry.end_time >= start_of_year:
                balance.yearly_duration += cls.__get_duration(
                    entry=entry,
                    this_ts=this_ts,
                    start_time=max(last_ts, start_of_year),
                )

            # Monthly
            if entry.end_time is None or entry.end_time >= start_of_month:
                balance.monthly_duration += cls.__get_duration(
                    entry=entry,
                    this_ts=this_ts,
                    start_time=max(last_ts, start_of_month),
                )

            # Weekly
            if entry.end_time is None or entry.end_time >= start_of_week:
                balance.weekly_duration += cls.__get_duration(
                    entry=entry,
                    this_ts=this_ts,
                    start_time=max(last_ts, start_of_week),
                )

        balance.save()
        return balance
