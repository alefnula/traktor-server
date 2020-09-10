from django.contrib import admin

from traktor.admin import name
from traktor_server.models import History


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "project_name",
        "task_name",
        "user",
        "cumulative_duration",
        "yearly_duration",
        "monthly_duration",
        "weekly_duration",
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
        "cumulative_duration",
        "yearly_duration",
        "monthly_duration",
        "weekly_duration",
    )
    fieldsets = (
        (None, {"fields": ("timestamp", "user", "project_name", "task")}),
        (
            "Durations",
            {
                "fields": (
                    "cumulative_duration",
                    "yearly_duration",
                    "monthly_duration",
                    "weekly_duration",
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
