from django.db import models

# Create your models here.
from django.db import models
from nanoid import generate
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import HStoreField



def nanoid_generate():
    return generate(size=24)


class Project(models.Model):
    # 问卷项目
    id = models.CharField(_('系统编码'), max_length=25, default=nanoid_generate, primary_key=True)
    created_dt = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_dt = models.DateTimeField(_('更新时间'), auto_now=True)
    title = models.CharField(_('项目标题'), max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_dt']
        permissions = [
            ('create_survey', '创建问卷')
        ]

    def __str__(self):
        return f"<{self.id}> - <{self.title}>"


class Structure(models.Model):
    # 问卷结构
    pass


class Survey(models.Model):
    """
    调查问卷主体
    """
    id = models.CharField(_('系统编码'), max_length=25, default=nanoid_generate, primary_key=True)
    title = models.CharField(_('项目标题'), max_length=255)
    created_dt = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_dt = models.DateTimeField(_('更新时间'), auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='surveys', related_query_name='survey')
    version = models.IntegerField(_('版本'), default=1)
    release_dt = models.DateTimeField(_('发布时间'), null=True, blank=True)
    withdraw_dt = models.DateTimeField(_('撤销时间'), null=True, blank=True)
    status = models.IntegerField(_('状态'), default=0)

    class Meta:
        permissions = [
            ('publish_survey', '发布权限'),
            ('invite_user', '邀请编辑'),
        ]

    def __str__(self):
        return f"<{self.id}> -survey- <{self.title}>"


class Policy(models.Model):
    id = models.CharField(_('系统编码'), max_length=25, default=nanoid_generate, primary_key=True)
    survey = models.ManyToManyField(Survey, related_name='policies', related_query_name='policy')
    title = models.CharField(_('政策名称'), max_length=255)
    content = models.TextField(_('正文'))
    content_html = models.TextField(_('正文html'))

    def __str__(self):
        return f"""
            {self.title}, {self.content}
        """


class Page(models.Model):
    """
    一个问卷可能有多页
    """
    id = models.CharField(_('系统编码'), max_length=25, default=nanoid_generate, primary_key=True)
    gid = models.IntegerField(_('项目编码'))
    cid = models.CharField(_('问卷ID'), max_length=25)
    type = models.CharField(_('类型'), max_length=25)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='pages', related_query_name='page')
    _index = models.IntegerField(_('页数'), default=-1)
    data = HStoreField(default=dict)

    def __str__(self):
        return f"<{self.id}> -page{self._index}- <{self.survey.title}>"


class Question(models.Model):
    id = models.CharField(_('系统编码'), max_length=25, default=nanoid_generate, primary_key=True)
    cid = models.CharField(_('问卷ID'), max_length=25)
    gid = models.IntegerField(_('组ID'))
    seq = models.IntegerField(_('顺序'))
    title = models.CharField(_('题目'), max_length=255)
    type = models.CharField(_('类型'), max_length=25)
    fixed = models.BooleanField(default=False)
    _index = models.IntegerField(_('问卷顺序'), )
    required = models.BooleanField(_('必填'), default=True)
    disp_code = models.CharField(max_length=255)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",
                               related_query_name="%(app_label)s_%(class)ss", )
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",
                             related_query_name="%(app_label)s_%(class)ss", )
    stored = models.BooleanField(_('题库'), default=False)
    qtype = models.CharField(_('题目类型'), max_length=50)
    items = models.ManyToManyField('Option', related_name="%(app_label)s_%(class)s_related",
                                   related_query_name="%(app_label)s_%(class)ss", )
    default_q_timecost = models.IntegerField(_('默认答题时间'), default=2)

    class Meta:
        abstract = True

    def __str__(self):
        return f"<{self.id}> -{self.qtype}- <{self.title}>"


class Blank(Question):
    default_q_timecost = models.IntegerField(_('默认答题时间'), default=4)
    words_number_range = ArrayField(
        models.IntegerField(), size=2, default=list
    )
    qtype = models.CharField(_('题目类型'), max_length=50, default='blank')


class SelectBase(Question):
    jump_code = models.CharField(_('跳转代码'), max_length=255)
    pGroupGid = models.IntegerField(_('组ID'), default=0)
    codeSelect = models.BooleanField(_('代码选择'), default=True)
    group_align = models.CharField(_('分组排列'), default='vertical', max_length=50)
    column_value = models.IntegerField(_('列数'), default=1)
    vote_setting = models.BooleanField(default=False)
    options_random = models.BooleanField(default=True)

    # option_group_list
    # optionsBindEffect
    # optionsGroupEffect
    # options_group_random
    class Meta:
        abstract = True


class Single(SelectBase):
    answerStyle = models.CharField(_('答案格式'), default='', max_length=50)
    qtype = models.CharField(_('题目类型'), max_length=50, default='single')


class Multiple(SelectBase):
    qtype = models.CharField(_('题目类型'), max_length=50, default='multiple')
    options_range = models.JSONField(_('选项范围'), default=dict)
    # option_exclude_list
    # optionsExcludeEffect
    # dispSelect


def option_default_open_attrs():
    return {
        "type": 0,
        "unit": "",
        "range": [],
        "unique": "none",
        "required": True
    }


class Option(models.Model):
    id = models.CharField(_('系统编码'), max_length=25, default=nanoid_generate, primary_key=True)
    gid = models.IntegerField(_('项目编码'))
    seq = models.IntegerField(_('顺序'))
    oid = models.IntegerField(_('选项id'))
    type = models.CharField(_('类型'), max_length=25, default='O')
    disp_code = models.CharField(_('展示代码'), max_length=255, default='')
    open_attrs = models.JSONField(_('其他'), default=option_default_open_attrs)
    plaster_code = models.CharField(max_length=255)
