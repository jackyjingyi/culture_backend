from rest_framework import serializers
from django.conf import settings
from .models import GroupLevel, OrgGroup, Organization, Industry


class GroupLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupLevel
        fields = (
            'group_level_id', 'group_level_name', 'org', 'level_children_id', 'level_num', 'version_id'
        )



class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = (
            'id', 'name', 'code'
        )


class OrganizationSerializer(serializers.ModelSerializer):
    industry = IndustrySerializer(read_only=True)

    class Meta:
        model = Organization
        fields = (
            'id', 'org_code', 'name', 'parent', 'industry', 'is_active', 'is_dept', 'is_delete', 'date_joined',
            'expire_dt', 'creator', 'manager'
        )


class OrgGroupSerializer(serializers.ModelSerializer):
    org = OrganizationSerializer(read_only=True)
    class Meta:
        model = OrgGroup
        fields = (
            'id', 'org', 'group_name', 'group_code', 'group_status', 'group_level', 'group_parent', 'have_children',
            'leaf_flag'
        )