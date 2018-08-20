# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import importlib
import re
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from forms import create_model_form, UserCreationForm, UserChangeForm
from crm.models import UserProfile
from school_crm.settings import URL_LOGIN
import crm_admin
import plug


# Create your views here.


def register(request):

    user_create_form = UserCreationForm()

    if request.method == 'POST':
        user_create_form = UserCreationForm(request.POST)
        if user_create_form.is_valid():
            print type(user_create_form.save())
            return HttpResponseRedirect('login')

    return render(request, 'crm_admin/register.html', {'user_create_form': UserCreationForm})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user is not None:
                login(request, user)
                request.session['user_profile'] = user.email
                return HttpResponseRedirect('index')

    return render(request, 'crm_admin/login.html')


def user_logout(request):

    logout(request)

    return HttpResponseRedirect('login')


def user_settings(request):

    user_change_form = UserChangeForm(request.user)

    return render(request, 'crm_admin/settings.html')


def password_change(request, app_name, table_name, objects):

    error_dict = {}

    if request.method == 'POST':
        user_profile = UserProfile.objects.get(id=objects)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user_profile.set_password(password2)
            user_profile.save()
            return HttpResponseRedirect('login')
        else:
            error_dict['input_error'] = '两次密码输入不一致!'
            return render(request, 'crm_admin/password_change.html', {'error_dict': error_dict})

    return render(request, 'crm_admin/password_change.html')


@login_required(login_url=URL_LOGIN)
def index(request):

    user_profile = UserProfile.objects.filter(email=request.session.get('user_profile'))
    show_table = crm_admin.registered_models

    return render(request, 'crm_admin/index.html', {'show_table': show_table,
                                                    'user_profile': user_profile})


@login_required(login_url=URL_LOGIN)
def show_tables(request, app_name, table_name):

    admin_class = crm_admin.registered_models[app_name][table_name]

    if request.method == 'POST':
        if 'custom_func' in request.POST:
            selected_obj = str(request.POST.get('selected_obj', '')).split(',')
            print selected_obj
            custom_func = request.POST.get('custom_func')
            returner = getattr(admin_class, custom_func)
            return returner(admin_class(), request, selected_obj, app_name, table_name)

    table_object = plug.object_search(request, admin_class)
    filter_table, filter_dict = plug.object_filter(request, table_object)
    filter_table = plug.table_reorder(request, filter_table)

    try:
        list_per_page = table_object.__getattribute__(table_object, 'list_per_page')
    except TypeError:
        list_per_page = 5
        table_object = admin_class
    paginator = Paginator(filter_table, list_per_page)

    page = request.GET.get('page', 1)
    order_field = request.GET.get('o', '')

    url_parameter = ''
    for k, v in filter_dict.items():
        url_parameter += '%s=%s&' % (k, v)

    try:
        page_data = paginator.page(page)
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page_data = paginator.page(1)

    return render(request, 'crm_admin/show_tables.html', {'table_object': table_object,
                                                          'page_data': page_data,
                                                          'filter_dict': filter_dict,
                                                          'url_parameter': url_parameter,
                                                          'order_field': order_field,
                                                          'admin_class': admin_class})


@login_required(login_url=URL_LOGIN)
def object_change(request, app_name, table_name, objects):

    admin_class = crm_admin.registered_models[app_name][table_name]
    model_form = create_model_form(admin_class.model)
    form_parameter = admin_class.model.objects.get(id=objects)

    if request.method == 'POST':
        form_object = model_form(request.POST, instance=form_parameter)
        if form_object.is_valid():
            form_object.save()
    else:
        form_object = model_form(instance=form_parameter)

    return render(request, 'crm_admin/object_change.html', {'form_object': form_object,
                                                            'app_name': app_name,
                                                            'table_name': table_name,
                                                            'objects': objects,
                                                            'admin_class': admin_class})


@login_required(login_url=URL_LOGIN)
def object_add(request, app_name, table_name):

    admin_class = crm_admin.registered_models[app_name][table_name]
    model_form = create_model_form(request, admin_class)

    if request.method == 'POST':
        form_object = model_form(request.POST)
        if form_object.is_valid():
            form_object.save()
            redirect_url = '/crm_admin/%s/%s' % (app_name, table_name)
            return redirect(redirect_url)
    else:
        form_object = model_form()

        return render(request, 'crm_admin/object_add.html', {'form_object': form_object})


@login_required(login_url=URL_LOGIN)
def object_delete(request, app_name, table_name, objects_id):

    admin_class = crm_admin.registered_models[app_name][table_name]
    objects = admin_class.model.objects.get(id=objects_id)
    relation_list = admin_class.model._meta.fields_map.values()

    if request.method == 'POST':
        if request.POST.get('yes'):
            objects.delete()
            return HttpResponseRedirect('/crm_admin/%s/%s' % (app_name, table_name))
        else:
            return redirect('/crm_admin/%s/%s' % (app_name, table_name))

    return render(request, 'crm_admin/object_delete.html', {'object': objects,
                                                            'relation_list': relation_list})
