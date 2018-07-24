# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.simple_tag()
def render_header(admin_class, url_parameter, header):
    verbose_name = ''
    url_parameter = url_parameter + 'o=%s' % header
    fields = admin_class.model._meta.fields
    for filed in fields:
        if header == filed.name:
            verbose_name = filed.verbose_name

    header_object = '<a href="?%s" class="headers" style="text-decoration: none; color: black;">%s</a>' % (url_parameter, verbose_name)
    return mark_safe(header_object)


@register.simple_tag()
def render_verbose_name(admin_class, filter_field):
    verbose_name = ''
    fields = admin_class.model._meta.fields
    for filed in fields:
        if filter_field == filed.name:
            verbose_name = filed.verbose_name
    return verbose_name


@register.simple_tag()
def render_table_name(admin_class):

    return admin_class.model._meta.verbose_name


@register.simple_tag()
def get_models(admin_class):

    return admin_class.model.objects.all()


@register.simple_tag()
def create_lines(models, list_display, request):

    html = ''
    for header in list_display:
        field = models._meta.get_field(header)
        if field.choices:
            data = getattr(models, 'get_%s_display' % header)()
        else:
            data = getattr(models, header)
        if header == list_display[0]:
            inner_html = '<td><input type=checkbox value={id} tag=obj_checkbox> <td><a href={request_path}/{id2}/change>{data}</a></td>'.format(request_path=request.path,
                                                                                                                              id=models.id,
                                                                                                                              data=data,
                                                                                                                              id2=models.id)
        else:
            inner_html = '<td>%s</td>' % data

        html += inner_html

    return mark_safe(html)


@register.simple_tag()
def render_page_ele(loop_counter, page_data, url_parameter, order_field):

    if abs(page_data.number - loop_counter) <= page_data.paginator.num_pages - 2:
        ele_class = ""
        if page_data.number == loop_counter:
            ele_class = "active"

        if order_field == '':
            ele = '''<li class="%s"><a href="?%spage=%s">%s</a></li>''' % (ele_class, url_parameter, loop_counter, loop_counter)
        else:
            ele = '''<li class="%s"><a href="?%spage=%s&o=%s">%s</a></li>''' % (ele_class, url_parameter, loop_counter, order_field, loop_counter)

        return mark_safe(ele)

    return mark_safe('<li>...</li>')


@register.simple_tag()
def render_page_index(page_data):

    return mark_safe('''<li>%s/%s</li>''' % (page_data.number, page_data.paginator.num_pages))


@register.simple_tag()
def render_filter_ele(filter_field, admin_class, filter_dict):

    select_ele = '''<select class="form-control" name='%s' ><option value=''>----</option>''' % filter_field
    field_obj = admin_class.model._meta.get_field(filter_field)

    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            if filter_dict.get(filter_field) == str(choice_item[0]):
                selected = "selected"

            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_dict.get(filter_field) == str(choice_item[0]):
                selected = "selected"
            select_ele += "<option value='%s' %s>%s</option>" % (choice_item[0], selected, choice_item[1])
            selected = ''
    select_ele += "</select>"

    if type(field_obj).__name__ in ('DateTimeField', 'DateField'):
        selected = ''
        select_ele = "<select class='form-control' name='%s' ><option value=''>----</option>" % filter_field
        for date in admin_class.date_range_field:

            if filter_dict.get(filter_field) == str(date):
                selected = 'selected'
            select_ele += "<option value='%s' %s>%s天内</option>" % (date, selected, date)
            selected = ''
    select_ele += '</select>'

        # selected = ''
        # for choice_item in field_obj.get_choices():
        #     if filter_dict.get(filter_field) == str(choice_item[0]):
        #         selected = "selected"
        #     select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
        #     selected = ''

    return mark_safe(select_ele)
