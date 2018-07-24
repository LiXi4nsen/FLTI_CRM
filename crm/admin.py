# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Group
from django.contrib import admin
from crm_admin import forms
import models

# Register your models here.

admin.site.register(models.Customer)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Enrollment)
admin.site.register(models.Course)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord)
admin.site.register(models.Branch)
admin.site.register(models.Role)
admin.site.register(models.Payment)
# admin.site.register(models.UserProfile)
admin.site.register(models.Tag)
admin.site.register(models.StudyRecord)
admin.site.register(models.Menu)
admin.site.register(models.UserProfile, forms.UserAdmin)
admin.site.unregister(Group)

