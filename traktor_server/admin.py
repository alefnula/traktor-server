from django.contrib import admin

from traktor.admin import name
from traktor_server.models import Balance


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "user",
        "project_name",
        "task_name",
        "cumulative_time",
        "yearly_time",
        "monthly_time",
        "weekly_time",
        "daily_time",
    )
    list_filter = ["task__project__user__username"]
    ordering = ["-timestamp"]
    search_fields = [
        "task__project__user__username",
        "task__project__name",
        "task__name",
    ]
    readonly_fields = (
        "timestamp",
        "user",
        "project_name",
        "cumulative_time",
        "yearly_time",
        "monthly_time",
        "weekly_time",
        "daily_time",
    )
    fieldsets = (
        (None, {"fields": ("timestamp", "user", "project_name", "task")}),
        (
            "Durations",
            {
                "fields": (
                    "cumulative_time",
                    "yearly_time",
                    "monthly_time",
                    "weekly_time",
                    "daily_time",
                )
            },
        ),
    )

    @name("User")
    def user(self, obj):
        return obj.task.project.user

    @name("Project")
    def project_name(self, obj):
        return obj.task.project.name

    @name("Task")
    def task_name(self, obj):
        return obj.task.name
