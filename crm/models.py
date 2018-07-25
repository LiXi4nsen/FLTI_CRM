# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.


class Customer(models.Model):
    """客户信息表"""

    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='客户姓名')
    qq = models.CharField(max_length=64, unique=True, verbose_name='客户QQ')
    qq_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='QQ昵称')
    phone = models.CharField(max_length=32, blank=True, null=True, verbose_name='手机号码')
    source_choices = ((0, '转介绍'),
                      (1, 'qq群'),
                      (2, '官网'),
                      (3, '百度推广'),
                      (4, '51CTO'),
                      (5, '知乎'),
                      (6, '线下传单'))
    source = models.SmallIntegerField(choices=source_choices, verbose_name='客户来源')
    referral_from = models.CharField(max_length=32, blank=True, null=True, verbose_name='转介绍人联系方式')
    consult_course = models.ForeignKey('Course', verbose_name='咨询课程名称')
    consult_content = models.TextField(verbose_name='咨询内容详情')
    consultant = models.ForeignKey('UserProfile', verbose_name='从属销售')
    date = models.DateTimeField(auto_now_add=True, verbose_name='咨询时间')
    note = models.TextField(blank=True, null=True, verbose_name='跟进概况')
    tag = models.ManyToManyField('Tag', blank=True, verbose_name='标签')

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name = '客户表'
        verbose_name_plural = '客户表'


class Tag(models.Model):
    """标签表"""

    tag_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = '标签表'
        verbose_name_plural = '标签表'


class CustomerFollowUp(models.Model):
    """客户跟进表"""

    customer = models.ForeignKey('Customer')
    content = models.TextField(verbose_name='跟进内容')
    consultant = models.ForeignKey('UserProfile')
    date = models.DateTimeField(auto_now_add=True)
    intention_choices = ((0, '两周内报名'),
                         (1, '一个月内报名'),
                         (2, '暂无报名计划'))
    intention = models.SmallIntegerField(choices=intention_choices)

    def __str__(self):
        return '%s %s' % (self.customer.qq, self.intention)

    class Meta:
        verbose_name = '客户跟进表'
        verbose_name_plural = '客户跟进表'


class Course(models.Model):
    """课程表"""

    name = models.CharField(max_length=32, unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name='课程周期')
    outline = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程表'
        verbose_name_plural = '课程表'


class Branch(models.Model):
    """校区表"""

    name = models.CharField(max_length=32, unique=True)
    address = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '校区表'
        verbose_name_plural = '校区表'


class ClassList(models.Model):
    """班级表"""

    branch = models.ForeignKey('Branch')
    course = models.ForeignKey('Course')
    semester = models.PositiveSmallIntegerField(verbose_name='学期')
    teachers = models.ManyToManyField('UserProfile')
    class_type_choices = ((0, '线下'),
                          (1, '网络'))
    class_type = models.SmallIntegerField(choices=class_type_choices)
    start_date = models.DateField(verbose_name='开班日期', blank=True, null=True)

    def __str__(self):
        return '%s %s %s' % (self.branch, self.course, self.semester)

    class Meta:

        unique_together = ('branch', 'course', 'semester')
        verbose_name = '班级表'
        verbose_name_plural = '班级表'


class CourseRecord(models.Model):
    """课程记录表"""

    from_class = models.ForeignKey('ClassList', verbose_name='班级')
    day_num = models.PositiveSmallIntegerField(verbose_name='课程号')
    teacher = models.ForeignKey('UserProfile')
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=32, verbose_name='作业标题', blank=True, null=True)
    homework_content = models.TextField(verbose_name='作业内容', blank=True, null=True)
    out_line = models.TextField(verbose_name='课程大纲')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.from_class, self.day_num)

    class Meta:
        unique_together = ('from_class', 'day_num')
        verbose_name = '课程记录表'
        verbose_name_plural = '课程记录表'


class StudyRecord(models.Model):
    """学习情况记录表"""

    student = models.ForeignKey('Enrollment')
    course_record = models.ForeignKey('CourseRecord')
    attendance_choice = ((0, '正常出勤'),
                         (1, '迟到'),
                         (2, '缺勤'))
    attendance = models.SmallIntegerField(choices=attendance_choice, default=0)
    score_choices = ((100, 'S'),
                     (95, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (80, 'B'),
                     (75,  'C+'),
                     (70, 'C'),
                     (65, 'D+'),
                     (60, 'D'),
                     (0, 'E'))
    score = models.SmallIntegerField(choices=score_choices, default=60)
    note = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s %s' % (self.student, self.attendance, self.score)

    class Meta:
        verbose_name = '学习情况记录表'
        verbose_name_plural = '学习情况记录表'


class Enrollment(models.Model):
    """报名表"""

    customer = models.ForeignKey('Customer')
    class_enrolled = models.ForeignKey('ClassList', verbose_name='报名班级')
    consultant = models.ForeignKey('UserProfile', verbose_name='销售')
    contract_agree = models.BooleanField(default=False, verbose_name='学员是否同意条款')
    contract_approved = models.BooleanField(default=False, verbose_name='销售是否审核')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.customer, self.class_enrolled)

    class Meta:
        unique_together = ('customer', 'class_enrolled')
        verbose_name = '报名表'
        verbose_name_plural = '报名表'


class Payment(models.Model):
    """缴费记录表"""
    customer = models.ForeignKey('Customer')
    amount = models.PositiveIntegerField(verbose_name='缴费数额')
    course = models.ForeignKey('ClassList', verbose_name='所报课程')
    consultant = models.ForeignKey('UserProfile')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.customer, self.amount)

    class Meta:
        verbose_name = '缴费记录表'
        verbose_name_plural = '缴费记录表'


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, name=None, number=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name, number):

        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    """账户表"""

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    name = models.CharField(max_length=32, verbose_name='姓名')
    number = models.CharField(max_length=32, verbose_name='工号/学号')
    roles = models.ForeignKey('Role', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['number', 'name']

    def __str__(self):
        return self.email

    def get_short_name(self):

        return self.name

    def get_full_name(self):

        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = '账户表'
        verbose_name_plural = '账户表'


# class UserProfile(models.Model):
#     """账户表"""
#
#     user = models.OneToOneField(User)
#     name = models.CharField(max_length=32)
#     roles = models.ForeignKey('Role', blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = '账户表'
#         verbose_name_plural = '账户表'


class Role(models.Model):
    """角色表"""

    role_name = models.CharField(max_length=32, unique=True)
    show_menu = models.ManyToManyField('Menu', blank=True)

    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = '角色表'


class Menu(models.Model):
    """菜单表"""

    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64, unique=True)
    absolute_url = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单表'
        verbose_name_plural = '菜单表'


