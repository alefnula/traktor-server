from rest_framework import serializers

from tea_django.serializers.colored import (
    ColoredCreateSerializer,
    ColoredUpdateSerializer,
)

from traktor.models import Project, Task, Entry


# Project


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.slug

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Project
        fields = ["id", "user", "name", "color", "created_on", "updated_on"]


class ProjectCreateSerializer(ColoredCreateSerializer):
    name = serializers.CharField(max_length=255)


class ProjectUpdateSerializer(ColoredUpdateSerializer):
    name = serializers.CharField(
        max_length=255, required=False, allow_null=True
    )


# Task


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def get_user(self, obj) -> str:
        return obj.project.user.username

    def get_project(self, obj) -> str:
        return obj.project.slug

    def get_id(self, obj) -> str:
        return obj.slug

    class Meta:
        model = Task
        fields = [
            "user",
            "project",
            "id",
            "name",
            "color",
            "default",
            "created_on",
            "updated_on",
        ]


class TaskCreateSerializer(ColoredCreateSerializer):
    name = serializers.CharField(max_length=255)
    default = serializers.BooleanField(default=False, required=False)


class TaskUpdateSerializer(ColoredUpdateSerializer):
    name = serializers.CharField(
        max_length=255, required=False, allow_null=True
    )
    default = serializers.BooleanField(
        default=False, required=False, allow_null=True
    )


# Entry


class EntrySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()
    task = serializers.SerializerMethodField()
    running_time = serializers.SerializerMethodField()

    def get_user(self, obj) -> str:
        return obj.task.project.user.username

    def get_project(self, obj) -> str:
        return obj.task.project.slug

    def get_task(self, obj) -> str:
        return obj.task.slug

    def get_running_time(self, obj) -> str:
        return obj.running_time

    class Meta:
        model = Entry
        fields = [
            "user",
            "project",
            "task",
            "description",
            "notes",
            "start_time",
            "end_time",
            "duration",
            "running_time",
            "created_on",
            "updated_on",
        ]


# Report


class ReportSerializer(serializers.Serializer):
    user = serializers.CharField()
    project = serializers.CharField()
    task = serializers.CharField()
    duration = serializers.IntegerField()
    running_time = serializers.CharField()
