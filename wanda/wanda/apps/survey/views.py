import json, logging
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from guardian.shortcuts import assign_perm, get_users_with_perms, get_user_perms, remove_perm, get_perms
from guardian.core import ObjectPermissionChecker
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action
from rest_framework.reverse import reverse
from rest_framework.permissions import DjangoObjectPermissions, DjangoModelPermissions, \
    DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework import status
from guardian.shortcuts import assign_perm
from .models import Project, Survey
from .serializers import ProjectSerializer, SurveySerializer

User = get_user_model()


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'current': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data,
        })


class ProjectFilter(filters.FilterSet):
    class Meta:
        model = Project
        fields = "__all__"


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # pagination_class = SmallResultsSetPagination
    filterset_class = ProjectFilter
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def create(self, request, *args, **kwargs):

        data = request.data
        data['creator'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        user = self.request.user
        assign_perm('change_project', user, instance)



class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
