from rest_framework import serializers
from django.conf import settings
from .models import Project, Survey


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id', 'title', 'creator', 'company', 'created_dt', 'updated_dt'
        )


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = (
            'id', 'title', 'project', 'created_dt', 'updated_dt', 'version', 'release_dt', 'withdraw_dt', 'status'
        )

