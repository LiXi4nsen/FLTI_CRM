# -*- coding: utf-8 -*-
from django.db.models import Q
import datetime
from copy import deepcopy


def object_search(request, admin_class):

    search_key = request.GET.get('s', '')

    if search_key == '':
        return admin_class
    else:
        search_field = admin_class.search_field
        q = Q()
        q.connector = 'OR'
        for child in search_field:
            search_tuple = (child, search_key)
            q.children.append(search_tuple)
        table_object = admin_class.model.objects.filter(q)

        return table_object


def object_filter(request, admin_class):

    filter_dict = {}

    for k, v in request.GET.items():
        if v:
            filter_dict[k] = v

    filter_object_dict = deepcopy(filter_dict)
    if filter_object_dict.get('page'):
        del filter_object_dict['page']
    if filter_object_dict.get('o'):
        del filter_object_dict['o']
    if filter_object_dict.get('s'):
        del filter_object_dict['s']
    if filter_object_dict.get('date'):
        date_to = datetime.datetime.now()
        date_from = date_to - datetime.timedelta(days=int(filter_object_dict['date']))
        del filter_object_dict['date']
        filter_object_dict['date__range'] = (date_from, date_to)

    search_flag = request.GET.get('s', '')

    if search_flag == '':
        return admin_class.model.objects.filter(**filter_object_dict), filter_dict
    else:
        return admin_class.filter(**filter_object_dict), filter_dict


def table_reorder(request, table_object):

    order_condition = request.GET.get('o', '')
    if order_condition == '':
        pass
    else:
        table_object = table_object.order_by(order_condition)

    return table_object
