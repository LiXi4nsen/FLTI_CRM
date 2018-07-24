# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from crm import models
from django.shortcuts import HttpResponseRedirect, render, redirect, HttpResponse
from datetime import timedelta


registered_models = {}


class BaseAdmin(object):

    list_display = []
    list_filter = []
    list_per_page = ''
    search_field = []
    date_range_field = []
    custom_function_list = ['delete_all']
    readonly_fields = []

    def delete_all(self, request, objects, app_name, table_name):

        admin_class = registered_models[app_name][table_name]
        deleted_objects = []

        if request.POST.get('yes'):
            if request.POST.get('yes'):
                for objects_id in objects:
                    if objects_id in ['on', '']:
                        continue
                    else:
                        print objects_id
                        delete_obj = admin_class.model.objects.get(id=str(objects_id))
                        deleted_objects.append(delete_obj)
                for deleted_object in deleted_objects:
                    deleted_object.delete()
                return HttpResponseRedirect('/crm_admin/%s/%s' % (app_name, table_name))
            else:
                return redirect('/crm_admin/%s/%s' % (app_name, table_name))

        objects2 = ''
        for i in objects:
            objects2 += i+','
        objects = objects2

        return render(request, 'crm_admin/object_delete.html', {'object': objects,
                                                                'custom_func': 'delete_all',
                                                                'objects': objects})


class CustomerAdmin(BaseAdmin):

    list_display = ['name', 'qq', 'source', 'consult_course', 'note', 'date']
    list_filter = ['source', 'consultant', 'consult_course', 'date']
    search_field = ['name', 'qq', 'note']
    list_per_page = 5
    date_range_field = [1, 3, 7, 30, 90, 365]
    custom_function_list = ['delete_all', 'hello_world']
    readonly_fields = ['qq', 'consultant']

    def hello_world(self, request, objects, app_name, table_name):


        return HttpResponse('HelloWorld')


class UserProfileAdmin(BaseAdmin):

    list_filter = ['name']
    list_display = ['name']
    search_field = ['name']
    list_per_page = 5
    date_range_field = [3, 7, 30, 90, 365]
    custom_function_list = ['delete_all']


def register(model_class, admin_class):

    if model_class._meta.app_label not in registered_models:
        registered_models[model_class._meta.app_label] = {}
    admin_class.model = model_class
    registered_models[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer, CustomerAdmin)
register(models.UserProfile, UserProfileAdmin)


