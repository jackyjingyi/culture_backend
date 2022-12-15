from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from nanoid import generate


def nanoid_generate():
    return generate(size=24)


class Industry(models.Model):
    # h
    id = models.CharField(_('行业ID'), max_length=25, default=nanoid_generate, primary_key=True)
    name = models.CharField(_('行业名称'), max_length=20)
    code = models.IntegerField(_('行业代码'),)

    class Meta:
        db_table = 'Industry'


class Organization(models.Model):
    # 组织
    id = models.CharField(_('组织ID'), max_length=25, default=nanoid_generate, primary_key=True)
    org_code = models.CharField(_('组织代码'), unique=True, max_length=25)
    name = models.CharField(_('公司名称'), max_length=150, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children',
                               related_query_name='child', blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(_('激活'), default=True)
    is_dept = models.BooleanField(_('是否部门'), default=False)
    is_deleted = models.BooleanField(_('已删除'), default=False)
    date_joined = models.DateTimeField(_("加入时间"), default=timezone.now)
    expire_dt = models.DateTimeField(_("过期时间"), null=True)
    creator = models.CharField(_('创建人'), max_length=25, null=True, blank=True)
    manager = models.CharField(_('管理者'), max_length=25, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Organization'


class OrgGroup(models.Model):
    id = models.CharField(_('组ID'), max_length=25, default=nanoid_generate, primary_key=True)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    group_name = models.CharField(_('名称'), max_length=20)
    group_code = models.CharField(_('组代码'), max_length=20)
    group_status = models.IntegerField(_('状态'), default=0)
    group_level = models.ForeignKey('GroupLevel', on_delete=models.CASCADE)
    group_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children',
                                     related_query_name='child', blank=True)
    have_children = models.BooleanField(default=False)
    leaf_flag = models.BooleanField(default=True)

    class Meta:
        db_table = 'OrgGroup'


class GroupLevel(models.Model):
    # 链表结构
    group_level_id = models.CharField(_('组ID'), max_length=25, default=nanoid_generate, primary_key=True)
    group_level_name = models.CharField(_('分组名称'), max_length=15)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    level_children_id = models.CharField(_('子等级ID'), max_length=25, null=True, blank=True)
    level_num = models.IntegerField(_('等级'), default=0, help_text='顺序自增')
    version_id = models.IntegerField(_('版本'), default=0)

    class Meta:
        db_table = 'GroupLevel'
