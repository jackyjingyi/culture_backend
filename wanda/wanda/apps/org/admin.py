from django.contrib import admin
from .models import GroupLevel, OrgGroup, Organization

# Register your models here.
admin.site.register(GroupLevel)
admin.site.register(OrgGroup)
admin.site.register(Organization)