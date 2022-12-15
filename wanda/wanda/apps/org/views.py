import json, logging
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework import status
from guardian.shortcuts import assign_perm
from .models import Organization, GroupLevel, OrgGroup, Industry
from .serializers import OrganizationSerializer, OrgGroupSerializer, GroupLevelSerializer, IndustrySerializer

User = get_user_model()


class OrganizationFilter(filters.FilterSet):
    class Meta:
        model = Organization
        fields = "__all__"


class OrgnizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filterset_class = OrganizationFilter

    def create(self, request, *args, **kwargs):
        data = request.data
        data['creator'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(),)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)