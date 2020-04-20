import os
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.http import JsonResponse
from . import models
from django.core.paginator import Paginator
import datetime
import hashlib
import arrow
import time
import json
import collections
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import re


def alter(path, old_str, new_str):
    with open(path, "r", encoding="utf-8") as f1, open("%s.bak" % path, "w", encoding="utf-8") as f2:
        data = f1.read()
        new_header = data.replace(old_str, new_str)
        f2.write(new_header)
    os.remove(path)
    os.rename("%s.bak" % path, path)
    print('修改完成')

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username_login = request.POST.get('username')
        password_login = request.POST.get('password')
        user = authenticate(username=username_login, password=password_login)
        if (user is not None) and (user.is_active):
            login(request, user)
            request.session['user'] = username_login
            return render(request, 'moniter/index.html')
        else:
            return render(request, 'moniter/login.html')
    else:
        return render(request, 'moniter/login.html')


def logout_user(request):
    logout(request)
    return render(request, 'moniter/login.html')


def reg_user(request):
    if request.method == 'GET':
        return render(request, 'moniter/registered.html')
    else:
        username = request.POST.get('username')
        password = hashlib.md5(
            (request.POST.get('username') + request.POST.get('confirm_password')).encode(encoding='UTF-8')).hexdigest()
        email = request.POST.get('email')
        models.user.objects.create(username=username, password=password, email=email)
        return render(request, 'moniter/login.html')


def order_view(request, spider_id):
    if request.method == 'GET':
        data = models.important_source.objects.filter(id=spider_id)[0]
        content = {}
        content['spider_id'] = data.id
        content['source_name'] = data.source_name
        content['url'] = data.url
        content['owner'] = data.owner
        return render(request, 'moniter/order-view.html', {'data': content})
    elif request.method == 'POST':
        spider_id = request.POST.get('spider_id')
        source_name = request.POST.get('source_name')
        url = request.POST.get('url')
        owner = request.POST.get('owner')
        data = models.important_source.objects.filter(pk=spider_id)[0]
        data.source_name = source_name
        data.url = url
        data.owner = owner
        data.save()
        return render(request, 'moniter/welcome1.html')


def del_order_view(request, spider_id):
    models.important_source.objects.get(id=spider_id).delete()
    return render(request, 'moniter/welcome1.html')


def edit_order_view(request):
    source_name = request.POST.get('source_name')
    data_lists = []
    data_normal = {}
    data_all = models.important_source.objects.filter(source_name__icontains=source_name)
    for i in data_all:
        data_dic = collections.OrderedDict()  # 将普通字典转换为有序字典
        data_dic['id'] = i.id
        data_dic['source_name'] = i.source_name
        data_dic['url'] = i.url
        data_dic['dimensions'] = i.dimensions
        data_dic['yesterday_num'] = i.yesterday_num
        data_dic['today_num'] = i.today_num
        data_dic['owner'] = i.owner
        data_dic['last_select_time'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        data_lists.append(data_dic)
    data_normal['data'] = json.dumps(data_lists)
    return render(request, 'moniter/welcome2.html', {'data_normal': data_normal})


def show_result(request):
    return render(request, 'moniter/welcome2.html')


def table_data(request):
    data_lists = []
    data_normal = {}
    data_all = models.important_source.objects.all()
    for i in data_all:
        data_dic = collections.OrderedDict()  # 将普通字典转换为有序字典
        data_dic['id'] = i.id
        data_dic['source_name'] = i.source_name
        data_dic['url'] = i.url
        data_dic['dimensions'] = i.dimensions
        data_dic['yesterday_num'] = i.yesterday_num
        data_dic['today_num'] = i.today_num
        data_dic['owner'] = i.owner
        data_dic['last_select_time'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        data_lists.append(data_dic)
    data_normal['data'] = data_lists
    return JsonResponse(data_normal)


@login_required
def index(request):
    username = request.session.get('user', "")
    return render(request, 'moniter/index.html', {'username': username})


def welcome(request):
    return render(request, 'moniter/welcome.html')


def welcome_first(request):
    def getYesterday(num):
        today = datetime.date.today()
        twoday = datetime.timedelta(days=num)
        yesterday = today - twoday
        return str(yesterday)

    def getMonth(num):
        month = arrow.now()
        twomonth = month.shift(months=-num).format("YYYY-MM")
        return twomonth

    important_all = models.important_source.objects.all()

    if request.method == 'GET':
        new_num = {}
        one = models.data_count.objects.get(time_date=getYesterday(0), dimensions='开庭公告').count
        two = models.data_count.objects.get(time_date=getYesterday(1), dimensions='开庭公告').count
        three = models.data_count.objects.get(time_date=getYesterday(2), dimensions='开庭公告').count
        four = models.data_count.objects.get(time_date=getYesterday(3), dimensions='开庭公告').count
        five = models.data_count.objects.get(time_date=getYesterday(4), dimensions='开庭公告').count
        six = models.data_count.objects.get(time_date=getYesterday(5), dimensions='开庭公告').count
        seven = models.data_count.objects.get(time_date=getYesterday(6), dimensions='开庭公告').count
        eight = models.data_count.objects.get(time_date=getYesterday(7), dimensions='开庭公告').count

        new_num['one_num'] = one
        new_num['two_num'] = two
        new_num['three_num'] = three
        new_num['four_num'] = four
        new_num['five_num'] = five
        new_num['six_num'] = six
        new_num['seven_num'] = seven

        new_num['seven'] = seven - eight
        new_num['six'] = six - seven
        new_num['five'] = five - six
        new_num['four'] = four - five
        new_num['three'] = three - four
        new_num['two'] = two - three
        new_num['one'] = one - two

        new_num['one_day'] = getYesterday(0)
        new_num['two_day'] = getYesterday(1)
        new_num['three_day'] = getYesterday(2)
        new_num['four_day'] = getYesterday(3)
        new_num['five_day'] = getYesterday(4)
        new_num['six_day'] = getYesterday(5)
        new_num['seven_day'] = getYesterday(6)

        one_month_num = models.month_datacount.objects.get(time_date=getMonth(6), dimensions='开庭公告').count
        two_month_num = models.month_datacount.objects.get(time_date=getMonth(5), dimensions='开庭公告').count
        three_month_num = models.month_datacount.objects.get(time_date=getMonth(4), dimensions='开庭公告').count
        four_month_num = models.month_datacount.objects.get(time_date=getMonth(3), dimensions='开庭公告').count
        five_month_num = models.month_datacount.objects.get(time_date=getMonth(2), dimensions='开庭公告').count
        six_month_num = models.month_datacount.objects.get(time_date=getMonth(1), dimensions='开庭公告').count
        seven_month_num = models.month_datacount.objects.get(time_date=getMonth(0), dimensions='开庭公告').count

        new_num['one_month_count'] = one_month_num
        new_num['two_month_count'] = two_month_num
        new_num['three_month_count'] = three_month_num
        new_num['four_month_count'] = four_month_num
        new_num['five_month_count'] = five_month_num
        new_num['six_month_count'] = six_month_num
        new_num['seven_month_count'] = seven_month_num
        # print(one_month_num, two_month_num, three_month_num, four_month_num, five_month_num, six_month_num, seven_month_num)

        new_num['one_month_add'] = two_month_num - one_month_num
        new_num['two_month_add'] = three_month_num - two_month_num
        new_num['three_month_add'] = four_month_num - three_month_num
        new_num['four_month_add'] = five_month_num - four_month_num
        new_num['five_month_add'] = six_month_num - five_month_num
        new_num['six_month_add'] = seven_month_num - six_month_num

        new_num['one_month'] = getMonth(6)
        new_num['two_month'] = getMonth(5)
        new_num['three_month'] = getMonth(4)
        new_num['four_month'] = getMonth(3)
        new_num['five_month'] = getMonth(2)
        new_num['six_month'] = getMonth(1)
        new_num['seven_month'] = getMonth(0)

        dimensions = {}
        all_dimensions = models.registered.objects.all()
        dimensions_lists = []
        for i in all_dimensions:
            dimensions_lists.append(i.table_dimensions)
        dimensions['dimensions'] = dimensions_lists

        return render(request, 'moniter/welcome1.html',
                      {'new_num': new_num, 'dimensions': dimensions, 'important_all': important_all})

    elif request.method == 'POST':
        num = {}
        new_num = {}
        dimensions = request.POST.get('dimensions')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        type_check = request.POST.get('month')
        # print(dimensions, startdate, enddate, type_check)

        if type_check != 'month':
            one_month_num = models.month_datacount.objects.get(time_date=getMonth(6), dimensions='开庭公告').count
            two_month_num = models.month_datacount.objects.get(time_date=getMonth(5), dimensions='开庭公告').count
            three_month_num = models.month_datacount.objects.get(time_date=getMonth(4), dimensions='开庭公告').count
            four_month_num = models.month_datacount.objects.get(time_date=getMonth(3), dimensions='开庭公告').count
            five_month_num = models.month_datacount.objects.get(time_date=getMonth(2), dimensions='开庭公告').count
            six_month_num = models.month_datacount.objects.get(time_date=getMonth(1), dimensions='开庭公告').count
            seven_month_num = models.month_datacount.objects.get(time_date=getMonth(0), dimensions='开庭公告').count

            new_num['one_month_count'] = one_month_num
            new_num['two_month_count'] = two_month_num
            new_num['three_month_count'] = three_month_num
            new_num['four_month_count'] = four_month_num
            new_num['five_month_count'] = five_month_num
            new_num['six_month_count'] = six_month_num
            new_num['seven_month_count'] = seven_month_num
            # print(one_month_num, two_month_num, three_month_num, four_month_num, five_month_num, six_month_num, seven_month_num)

            new_num['one_month_add'] = two_month_num - one_month_num
            new_num['two_month_add'] = three_month_num - two_month_num
            new_num['three_month_add'] = four_month_num - three_month_num
            new_num['four_month_add'] = five_month_num - four_month_num
            new_num['five_month_add'] = six_month_num - five_month_num
            new_num['six_month_add'] = seven_month_num - six_month_num

            new_num['one_month'] = getMonth(6)
            new_num['two_month'] = getMonth(5)
            new_num['three_month'] = getMonth(4)
            new_num['four_month'] = getMonth(3)
            new_num['five_month'] = getMonth(2)
            new_num['six_month'] = getMonth(1)
            new_num['seven_month'] = getMonth(0)

            date_num = []
            start_year = int(startdate[:4])
            start_month = int(startdate[5:7])
            start_day = int(startdate[8:10])
            end_month = int(enddate[5:7])
            end_day = int(enddate[8:10])
            date_num.append(start_month)
            date_num.append(start_day)
            date_num.append(end_month)
            date_num.append(end_day)
            for i in date_num:
                if str(i).endswith('0') == True:
                    pass
                else:
                    continue
            # print(start_year, start_month, start_day, end_month, end_day)
            for d in range(start_year, start_year + 1):
                begin = datetime.date(d, start_month, start_day)
                end = datetime.date(d, end_month, end_day)
                for k, v in enumerate(range((end - begin).days + 1)):
                    day = begin + datetime.timedelta(days=v)
                    data = models.data_count.objects.get(time_date=day, dimensions=dimensions)
                    num[k] = data.count
                    # print(day, dimensions, data.count)

            one_num = num[0]
            two_num = num[1]
            three_num = num[2]
            four_num = num[3]
            five_num = num[4]
            six_num = num[5]
            seven_num = num[6]
            eight_num = models.data_count.objects.get(time_date=getYesterday(7), dimensions=dimensions).count

            new_num['one_num'] = seven_num
            new_num['two_num'] = six_num
            new_num['three_num'] = five_num
            new_num['four_num'] = four_num
            new_num['five_num'] = three_num
            new_num['six_num'] = two_num
            new_num['seven_num'] = one_num
            new_num['eight_num'] = eight_num

            new_num['seven'] = one_num - eight_num
            new_num['six'] = two_num - one_num
            new_num['five'] = three_num - two_num
            new_num['four'] = four_num - three_num
            new_num['three'] = five_num - four_num
            new_num['two'] = six_num - five_num
            new_num['one'] = seven_num - six_num

            new_num['one_day'] = getYesterday(0)
            new_num['two_day'] = getYesterday(1)
            new_num['three_day'] = getYesterday(2)
            new_num['four_day'] = getYesterday(3)
            new_num['five_day'] = getYesterday(4)
            new_num['six_day'] = getYesterday(5)
            new_num['seven_day'] = getYesterday(6)

            dimensions_map = {}
            all_dimensions = models.registered.objects.all()
            dimensions_lists = []
            for i in all_dimensions:
                dimensions_lists.append(i.table_dimensions)
            dimensions_map['dimensions'] = dimensions_lists

            info = {'staartdate': startdate, 'endate': enddate, 'dimensions_name': dimensions}
            return render(request, 'moniter/welcome1.html',
                          {'new_num': new_num, 'dimensions': dimensions_map, 'info': info,
                           'important_all': important_all})

        elif type_check == 'month':
            one = models.data_count.objects.get(time_date=getYesterday(0), dimensions='开庭公告').count
            two = models.data_count.objects.get(time_date=getYesterday(1), dimensions='开庭公告').count
            three = models.data_count.objects.get(time_date=getYesterday(2), dimensions='开庭公告').count
            four = models.data_count.objects.get(time_date=getYesterday(3), dimensions='开庭公告').count
            five = models.data_count.objects.get(time_date=getYesterday(4), dimensions='开庭公告').count
            six = models.data_count.objects.get(time_date=getYesterday(5), dimensions='开庭公告').count
            seven = models.data_count.objects.get(time_date=getYesterday(6), dimensions='开庭公告').count
            eight = models.data_count.objects.get(time_date=getYesterday(7), dimensions='开庭公告').count

            new_num['one_num'] = one
            new_num['two_num'] = two
            new_num['three_num'] = three
            new_num['four_num'] = four
            new_num['five_num'] = five
            new_num['six_num'] = six
            new_num['seven_num'] = seven

            new_num['seven'] = seven - eight
            new_num['six'] = six - seven
            new_num['five'] = five - six
            new_num['four'] = four - five
            new_num['three'] = three - four
            new_num['two'] = two - three
            new_num['one'] = one - two

            new_num['one_day'] = getYesterday(0)
            new_num['two_day'] = getYesterday(1)
            new_num['three_day'] = getYesterday(2)
            new_num['four_day'] = getYesterday(3)
            new_num['five_day'] = getYesterday(4)
            new_num['six_day'] = getYesterday(5)
            new_num['seven_day'] = getYesterday(6)

            dimensions = request.POST.get('dimensions')
            startdate = request.POST.get('startmonth')
            enddate = request.POST.get('endmonth')
            start_year = int(startdate[:4])
            start_month = int(startdate[5:7].replace('0', ''))
            end_month = int(enddate[5:7].replace('0', ''))
            for d in range(start_year, start_year + 1):
                for k, m in enumerate(range(start_month, end_month + 1)):
                    if m >= 10:
                        month = str(start_year) + "-" + str(m)
                    else:
                        month = str(start_year) + "-0" + str(m)
                    data = models.month_datacount.objects.get(time_date=month, dimensions=dimensions)
                    num[k] = data.count

            one_month_num = num[0]
            two_month_num = num[1]
            three_month_num = num[2]
            four_month_num = num[3]
            five_month_num = num[4]
            six_month_num = num[5]
            if end_month == 12:
                seven_month_num = models.month_datacount.objects.get(time_date=enddate, dimensions=dimensions).count
            else:
                start_month = start_month - 1
                if start_month < 10:
                    time_date = str(start_year) + "-0" + str(start_month)
                else:
                    time_date = str(start_year) + "-" + str(start_month)
                seven_month_num = models.month_datacount.objects.get(time_date=time_date, dimensions=dimensions).count
            # print(enddate, six_month_num, seven_month_num)

            new_num['one_month_count'] = one_month_num
            new_num['two_month_count'] = two_month_num
            new_num['three_month_count'] = three_month_num
            new_num['four_month_count'] = four_month_num
            new_num['five_month_count'] = five_month_num
            new_num['six_month_count'] = six_month_num
            new_num['seven_month_count'] = seven_month_num
            # print(one_month_num, two_month_num, three_month_num, four_month_num, five_month_num, six_month_num, seven_month_num)

            new_num['one_month_add'] = one_month_num - seven_month_num
            new_num['two_month_add'] = two_month_num - one_month_num
            new_num['three_month_add'] = three_month_num - two_month_num
            new_num['four_month_add'] = four_month_num - three_month_num
            new_num['five_month_add'] = five_month_num - four_month_num
            new_num['six_month_add'] = six_month_num - five_month_num

            new_num['one_month'] = getMonth(6)
            new_num['two_month'] = getMonth(5)
            new_num['three_month'] = getMonth(4)
            new_num['four_month'] = getMonth(3)
            new_num['five_month'] = getMonth(2)
            new_num['six_month'] = getMonth(1)
            new_num['seven_month'] = getMonth(0)

            dimensions_map = {}
            all_dimensions = models.registered.objects.all()
            dimensions_lists = []
            for i in all_dimensions:
                dimensions_lists.append(i.table_dimensions)
            dimensions['dimensions'] = dimensions_lists

            infos = {'startmonth': startdate, 'endmonth': enddate, 'dimensions_name': dimensions}
            return render(request, 'moniter/welcome1.html',
                          {'new_num': new_num, 'dimensions': dimensions_map, 'infos': infos,
                           'important_all': important_all})


def order(request):
    if request.POST:
        projectname = request.POST.get('projectname')
        spider_count = request.POST.get('count')
        creattime = request.POST.get('creattime')
        user = request.POST.get('user')
        contrller = request.POST.get('contrller')
        desc = request.POST.get('desc')
        import os
        path = os.getcwd() + '\project_filed'
        os.popen('cd {path} & scrapy startproject {projectname}'.format(path=path, projectname=projectname))
        # os.popen('cd {} & scrapy genspider ttt qweqwe')
        models.creat_project_lists.objects.create(project_name=projectname, spider_count=spider_count,
                                                  project_desc=desc, created_time=creattime, owner=user,
                                                  contrller=contrller)
    all_project = models.creat_project_lists.objects.all()
    return render(request, 'moniter/order-list.html', {'order_lists': all_project})


def ceshi(request):
    return render(request, 'moniter/ceshi.html')


def order_add(request):
    # os.system('scrapy startproject yshysh & cd yshysh & scrapy genspider ttt qweqwe')
    return render(request, 'moniter/order-add.html')


def spider(request):
    if request.POST:
        projectname = request.POST.get('projectname')
        spidername = request.POST.get('spidername')
        is_incremental = request.POST.get('is_incremental')
        interval = request.POST.get('interval')
        is_insert = request.POST.get('is_insert')
        table = request.POST.get('table')
        spiderdesc = request.POST.get('spiderdesc')
        import os
        m = """# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from urllib.request import urljoin
from ..items import *


class {classname}Spider(scrapy.Spider):
    name = '{spidername}'
    interval = {interval}
    IS_INSERT = {is_insert}
    IS_INCREMENTAL = {is_incremental}
    table = '{table}'
        
    def start_requests(self):
        url = 'start_url'
        yield scrapy.Request(url=url, callback=self.get_page)
        
    def get_page(self, response):
        s = Selector(response=response)
        for i in range(1, int(pages)+1):
            yield scrapy.Request(url=i, callback=self.get_lists)
    
    def get_lists(self, response):
        s = Selector(response=response)
        lists = s.xpath('lists_xpath')
        for i in lists:
            href = urljoin(response.url, i.xpath('content_xpath').extract_first())
            if href:
                yield scrapy.Request(url=href, callback=self.get_contents)
    
    def get_contents(self, response):
        item = {item_name}Item()
        s = Selector(response=response)
        """
        path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\spiders\{spidername}.py'.format(projectname=projectname, projectname_1=projectname, spidername=spidername)
        with open(path, 'wb') as file:
            file.write(m.format(projectname_one=projectname, projectname_two=projectname, classname=spidername.capitalize(), spidername=spidername, interval=interval, is_insert=is_insert, is_incremental=is_incremental, table=table, item_name=projectname.capitalize()).encode('utf-8'))
        models.creat_spider_lists.objects.create(projectname=projectname, spidername=spidername, islong=is_incremental, spiderdesc=spiderdesc, creattime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    all_spider = models.creat_spider_lists.objects.all()
    return render(request, 'moniter/spider_lists.html', {'spider_lists': all_spider})


def spider_add(request, project_name):
    # os.system('scrapy startproject yshysh & cd yshysh & scrapy genspider ttt qweqwe')
    all_spider = models.creat_project_lists.objects.all()
    project_lists = []
    for i in all_spider:
        project_lists.append(i.project_name)
    return render(request, 'moniter/spider_add.html', {'project_name': project_name, 'project_lists': project_lists})


def spider_info(request, project_name, spider_id, spider_name):
    all_project = models.creat_project_lists.objects.all()
    all_prarm = models.spider_prarm.objects.all()
    return render(request, 'moniter/spider_info.html',
                  {'project_name': project_name, 'spider_id': spider_id, "spider_name": spider_name,
                   "project_lists": all_project, 'all_prarm': all_prarm})


def spider_info_data(request, spider_name):
    a = {"code": 0, "msg": "", "count": 1000, "data": []}
    all_spdier = models.creat_spider_lists.objects.filter(spidername=spider_name)
    for i in all_spdier:
        a.get('data').append(
            {"node": i.node, "spdiername": i.spidername, "param": i.param, "count": i.count, "status": i.laststatus,
             "creattime": i.creattime})
    return JsonResponse(a)


def spider_setting(request, spider_name):
    a = {"code": 0, "msg": "", "count": 1000, "data": [
        # {"varname": '10000', "vartype": "user-0", "varvalue": "女"}
    ]}
    all_param = models.spider_prarm.objects.filter(spidername=spider_name)
    for i in all_param:
        a.get('data').append({'id': i.id, "varname": i.varname, "vartype": i.vartype, "varvalue": i.varvalue})
    return JsonResponse(a)

def del_param(request, spider_name, varname):
    param = models.spider_prarm.objects.filter(spidername=spider_name, varname=varname)
    if param:
        param.delete()
    return render(request, 'moniter/spider_info.html', {'spider_name': spider_name})

def add_param_html(request, project_name, spider_name):
    return render(request, 'moniter/add_param.html', {'project_name': project_name, 'spider_name': spider_name})

def add_param(request):
    if request.POST:
        project_name = request.POST.get('projectname')
        spider_name = request.POST.get('spidername')
        varname = request.POST.get('varname')
        vartype = request.POST.get('vartype')
        varvalue = request.POST.get('varvalue')
        path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\spiders\{spidername}.py'.format(projectname=project_name, projectname_1=project_name, spidername=spider_name)
        path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\settings.py'.format(projectname=project_name, projectname_1=project_name)
        with open(path, mode='a') as filename:
            filename.write(varname+' = '+varvalue)
            filename.write('\n')  # 换行
        models.spider_prarm.objects.create(spidername=spider_name, varname=varname, vartype=vartype, varvalue=varvalue)
    return render(request, 'moniter/spider_info.html')

def del_start(request, spider_name, spider_id):
    url = models.spider_start.objects.filter(spidername=spider_name, pk=spider_id)
    if url:
        url.delete()
    return render(request, 'moniter/spider_info.html', {'spider_name': spider_name})

def add_config_html(request, project_name, spider_name):
    return render(request, 'moniter/add_config.html', {'project_name': project_name, 'spider_name': spider_name})

def add_config(request):
    if request.POST:
        project_name = request.POST.get('projectname')
        spider_name = request.POST.get('spidername')
        starturl = request.POST.get('starturl')
        requesttype = request.POST.get('requesttype')
        headers = request.POST.get('headers')
        formdata = request.POST.get('formdata')
        path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\spiders\{spidername}.py'.format(projectname=project_name, projectname_1=project_name, spidername=spider_name)
        # alter(path, 'pass1', "self.headers = {"+ '{headers_demo}'.format(headers_demo=headers.replace('\n', '')) + "}")
        alter(path, 'start_url', starturl)
        if requesttype == 'GET':
            alter(path, 'pass3', 'yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)')
        elif requesttype == 'POST':
            data = """formdata = {{formdata}}""".format(formdata=formdata)
            alter(path, 'pass3', 'yield scrapy.FormRequest(url=url, formdata={formdata}, headers=self.headers, callback=self.parse)'.format(formdata=data))
        models.spider_start.objects.create(spidername=spider_name, startrequest=starturl, requesttype=requesttype, headers=headers, formdata=formdata)
    return render(request, 'moniter/spider_info.html')

# def edit_config(request, project_name, spider_name, spider_id, startrequest, headers, requesttype, formdata):
def edit_config(request):
    if request.POST:
        project_name = request.POST.get('project_name')
        spider_name = request.POST.get('spider_name')
        spider_id = request.POST.get('spider_id')
        startrequest = request.POST.get('startrequest')
        headers_demo = request.POST.get('headers')
        requesttype = request.POST.get('requesttype')
        formdata = request.POST.get('formdata')
        path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\spiders\{spiders}.py'.format(projectname=project_name, projectname_1=project_name, spiders=spider_name)
        config_info = models.spider_start.objects.filter(pk=spider_id)[0]
        alter(path, config_info.startrequest, startrequest)
        alter(path, config_info.headers, headers_demo, header_rule=True)
        alter(path, config_info.formdata, formdata)
        config_info.startrequest = startrequest
        config_info.headers = headers_demo
        config_info.requesttype = requesttype
        config_info.formdata = formdata
        config_info.save()
    return render(request, 'moniter/spider_info.html')


def start_json(request, spider_name):
    a = {"code": 0, "msg": "", "count": 1000, "data": []}
    all_start = models.spider_start.objects.filter(spidername=spider_name)
    for i in all_start:
        a.get('data').append({
            "id": i.id,
            "startrequest": i.startrequest,
            "headers": """{headers}""".format(headers=i.headers),
            "requesttype": i.requesttype,
            "formdata": ''
        })
    return JsonResponse(a)

def del_pageset(request, spider_name, spider_id):
    url = models.page_set.objects.filter(spidername=spider_name, pk=spider_id)
    if url:
        url.delete()
    return render(request, 'moniter/spider_info.html', {'spider_name': spider_name})

def add_pagepath_html(request, project_name, spider_name):
    return render(request, 'moniter/add_pagepath.html', {'project_name': project_name, 'spider_name': spider_name})

def add_pagepath(request):
    if request.POST:
        project_name = request.POST.get('projectname')
        spider_name = request.POST.get('spidername')
        pageurl = request.POST.get('pageurl')
        pagecount = request.POST.get('pagecount')
        pagevar = request.POST.get('pagevar')
        callname = request.POST.get('callname')
        path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\spiders\{spidername}.py'.format(projectname=project_name, projectname_1=project_name, spidername=spider_name)
        alter(path, 'pages', pagecount)
        models.page_set.objects.create(spidername=spider_name, pageurl=pageurl, pagecount=pagecount, pagevar=pagevar, callname=callname)
    return render(request, 'moniter/spider_info.html')

def filed_data(request, spider_name):
    a = {"code": 0, "msg": "", "count": 1000, "data": []}
    all_data = models.content_set.objects.filter(spidername=spider_name)
    for i in all_data:
        a.get('data').append({
            "id": i.id,
            "spidername": i.spidername,
            "fieldname": i.fieldname,
            "rule": i.rule,
            "is_many": i.is_many,
            "notename": i.notename
        })
    return JsonResponse(a)

def del_filedset(request, spider_name, spider_id):
    url = models.content_set.objects.filter(spidername=spider_name, pk=spider_id)
    if url:
        url.delete()
    return render(request, 'moniter/spider_info.html', {'spider_name': spider_name})

def add_filed_html(request, project_name, spider_name):
    return render(request, 'moniter/add_filed.html', {'project_name': project_name, 'spider_name': spider_name})

def add_filedpath(request):
    if request.POST:
        project_name = request.POST.get('projectname')
        spider_name = request.POST.get('spidername')
        fieldname = request.POST.get('fieldname')
        rule = request.POST.get('rule')
        is_many = request.POST.get('is_many')
        notename = request.POST.get('notename')
        path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\spiders\{spidername}.py'.format(projectname=project_name, projectname_1=project_name, spidername=spider_name)
        with open(path, mode='a') as f:
            f.write('\n        ')  # 换行
            if is_many == '多个':
                f.write(fieldname+' = '+ 's.xpath("'+ rule.replace('"', "'")+'").extract()')
            else:
                f.write(fieldname+' = '+ 's.xpath("'+ rule.replace('"', "'")+'").extract_first("")')
            f.write('\n        ')  # 换行
            f.write('item["{filename_item}"] = {filename}'.format(filename_item=fieldname, filename=fieldname))
            f.write('\n        ')  # 换行
        models.content_set.objects.create(spidername=spider_name, fieldname=fieldname, rule=rule, notename=notename)
    return render(request, 'moniter/spider_info.html')

def down_add(request):
    if request.POST:
        project_name = request.POST.get('project_name')
        spider_name = request.POST.get('spider_name')
        down = request.POST.get('down')
        if down == 'yes':
            path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\spiders\{spidername}.py'.format(projectname=project_name, projectname_1=project_name, spidername=spider_name)
            with open(path, mode='a') as f:
                f.write('\n        ')  # 换行
                f.write('yield item')
    return render(request, 'moniter/spider_info.html')

def page_data(request, spider_name):
    a = {"code": 0, "msg": "", "count": 1000, "data": []}
    all_data = models.page_set.objects.filter(spidername=spider_name)
    for i in all_data:
        a.get('data').append({
            "id": i.id,
            "spidername": i.spidername,
            "pageurl": i.pageurl,
            "pagecount": i.pagecount,
            "pagevar": i.pagevar,
            "callname": i.callname
        })
    return JsonResponse(a)

def del_listsset(request, spider_name, spider_id):
    url = models.lists_set.objects.filter(spidername=spider_name, pk=spider_id)
    if url:
        url.delete()
    return render(request, 'moniter/spider_info.html', {'spider_name': spider_name})

def add_lists_html(request, project_name, spider_name):
    return render(request, 'moniter/add_lists.html', {'project_name': project_name, 'spider_name': spider_name})

def add_listspath(request):
    if request.POST:
        project_name = request.POST.get('projectname')
        spider_name = request.POST.get('spidername')
        listsxpath = request.POST.get('listsxpath')
        contentxpath = request.POST.get('contentxpath')
        callname = request.POST.get('callname')
        path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\spiders\{spidername}.py'.format(projectname=project_name, projectname_1=project_name, spidername=spider_name)
        alter(path, 'lists_xpath', listsxpath)
        alter(path, 'content_xpath', contentxpath)
        models.lists_set.objects.create(spidername=spider_name, listsxpath=listsxpath, contentxpath=contentxpath, callname=callname)
    return render(request, 'moniter/spider_info.html')

def lists_data(request, spider_name):
    a = {"code": 0, "msg": "", "count": 1000, "data": []}
    all_data = models.lists_set.objects.filter(spidername=spider_name)
    for i in all_data:
        a.get('data').append({
            "id": i.id,
            "listsxpath": i.listsxpath,
            "contentxpath": i.contentxpath,
            "callname": i.callname
        })
    return JsonResponse(a)

def edit_param(request, project_name, spider_name, param_id, varname, vartype, varvalue):
    path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\settings.py'.format(projectname=project_name, projectname_1=project_name)
    param_info = models.spider_prarm.objects.filter(pk=param_id)[0]
    if '注释' in varname:
        varname = '#'+ varname.replace('注释', '')
    alter(path, param_info.varname + ' = '+param_info.varvalue, varname+' = '+varvalue)
    param_info.varname = varname
    param_info.vartype = vartype
    param_info.varvalue = varvalue
    param_info.save()
    return render(request, 'moniter/spider_info.html')

def edit_spider(request, spider_id, project_name):
    return render(request, 'moniter/edit_spider.html', {'spider_id': spider_id, 'projectname': project_name})


def spider_refix(request, spider_refix_id):
    if request.POST:
        spider_id = request.POST.get('spider_id')
        projectname = request.POST.get('projectname')
        spidername = request.POST.get('spidername')
        islong = request.POST.get('islong')
        # contrller = request.POST.get('contrller')
        spiderdesc = request.POST.get('spiderdesc')
        spider_data = models.creat_spider_lists.objects.filter(pk=spider_id)[0]
        path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\spiders'.format(projectname=projectname,
                                                                                           projectname_1=projectname)
        spider = os.path.join(path, spider_data.spidername + '.py')
        dirname, filename = os.path.split(spider)
        new_file = os.path.join(dirname, spidername + '.py')
        os.rename(spider, new_file)

        m = """# -*- coding: utf-8 -*-
import scrapy


class {classname}Spider(scrapy.Spider):
    name = "{spidername}"
    interval = {interval}  # 增量间隔
    IS_INSERT = {IS_INSERT}  # 时候是第一次运行插入
    IS_INCREMENTAL = {IS_INCREMENTAL}  # 是否开启增量
    table = '{table}'  # 插入的表名

    def start_requests(self):
        pass

    def parse(self, response):
        pass
                """
        path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\spiders\{spidername}.py'.format(
            projectname=projectname, projectname_1=projectname, spidername=spidername)
        # os.popen('cd {path} & scrapy genspider {spidername} baidu.com'.format(path=path, spidername=spidername))
        with open(path, 'wb') as file:
            file.write(
                m.format(classname=spidername.capitalize(), spidername=spidername, interval=1440, IS_INSERT='True',
                         IS_INCREMENTAL='True', table='caipan').encode('utf-8'))

        spider_data.projectname = projectname
        spider_data.spidername = spidername
        spider_data.islong = islong
        spider_data.spiderdesc = spiderdesc
        spider_data.save()
    if spider_refix_id == 1:
        all_spider = models.creat_spider_lists.objects.all()
        return render(request, 'moniter/spider_lists.html', {'spider_lists': all_spider})
    else:
        all_spider = models.creat_spider_lists.objects.all()
        return render(request, 'moniter/order-list1.html', {'spider_lists': all_spider})


def spider_del_one(request, spider_id):
    spider = models.creat_spider_lists.objects.filter(pk=spider_id)[0]
    project_name = spider.projectname
    spider_name = spider.spidername
    path = os.getcwd() + '\project_filed\{project_name}\{project_name_1}\spiders\{spider_name}'.format(
        project_name=project_name, project_name_1=project_name, spider_name=spider_name + '.py')
    os.system('del /a/f/q "{path}"'.format(path=path))
    spider.delete()
    all_spider = models.creat_spider_lists.objects.all()
    return render(request, 'moniter/order-list1.html', {'spider_lists': all_spider})


def spider_del(request):
    if request.POST:
        spider_id = request.POST.get('spider_id')
        spider = models.creat_spider_lists.objects.filter(pk=spider_id)[0]
        project_name = spider.projectname
        spider_name = spider.spidername
        path = os.getcwd() + '\project_filed\{project_name}\{project_name_1}\spiders\{spider_name}'.format(
            project_name=project_name, project_name_1=project_name, spider_name=spider_name + '.py')
        os.system('del /a/f/q "{path}"'.format(path=path))
        spider.delete()
    all_spider = models.creat_spider_lists.objects.all()
    return render(request, 'moniter/spider_lists.html', {'spider_lists': all_spider})


def spider_del_info(request, spider_id):
    return render(request, 'moniter/spider_del_info.html', {'spider_id': spider_id})


def order_del(request, project_id):
    project_idlists = project_id.split(',')
    for i in project_idlists:
        project_lists = models.creat_project_lists.objects.filter(id=i)
        for p in project_lists:
            project_name = p.project_name
            path = os.getcwd() + '\project_filed\{project_name}'.format(project_name=project_name)
            os.system('rmdir /s/q {path}'.format(path=path))
        project_lists.delete()
    all_project = models.creat_project_lists.objects.all()
    return render(request, 'moniter/order-list.html', {'order_lists': all_project})


def spider_lists(request, project_id, project_name):
    return render(request, 'moniter/spider_lists.html', {'project_id': project_id, 'project_name': project_name})


def first_order(request, project_id):
    if project_id == '999999999999':
        all_spider = models.creat_spider_lists.objects.all()
        return render(request, 'moniter/order-list1.html', {'project_id': project_id, 'spider_lists': all_spider})


def first_order_view(request, spider_id, project_name):
    return render(request, 'moniter/order-view_1.html', {'spider_id': spider_id, 'projectname': project_name})


def cate(request):
    return render(request, 'moniter/cate.html')


def member(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    all_spider = models.spider_lists.objects.all()
    paginator = Paginator(all_spider, 10)
    page_num = paginator.num_pages
    page_spider_list = paginator.page(page)
    if page_spider_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_spider_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page
    return render(request, 'moniter/member-list.html', {'all_spider': page_spider_list,
                                                        'page_num': range(1, page_num + 1),
                                                        'curr_page': page,
                                                        'next_page': next_page,
                                                        'previous_page': previous_page
                                                        })


def del_data(request, spider_id):
    models.spider_lists.objects.filter(id=spider_id).delete()
    return render(request, 'moniter/member-list.html')


def edit_status(request, spider_name):
    spider_data = models.spider_lists.objects.filter(spider_name=spider_name)[0]
    if spider_data.status == 0:
        spider_data.status = 1
    else:
        spider_data.status = 0
    spider_data.save()
    return render(request, 'moniter/member-list.html')


def edit(request, spider_id):
    data = {}
    spider_data = models.spider_lists.objects.filter(pk=spider_id)[0]
    data['spider_id'] = spider_id
    data['servers'] = [
        '106.75.18.196',
        '106.75.123.173',
        '106.50.40.174',
        '106.75.100.246'
    ]
    data['interval_time'] = spider_data.interval_time
    data['data_base'] = spider_data.data_base
    data['server'] = spider_data.server
    return render(request, 'moniter/member-edit.html', {'data': data})


def edit_action(request):
    spider_id = request.POST.get('spider_id')
    interval_time = request.POST.get('interval_time')
    data_base = request.POST.get('data_base')
    server = request.POST.get('server')
    spider_data = models.spider_lists.objects.filter(pk=spider_id)[0]
    spider_data.interval_time = interval_time
    spider_data.data_base = data_base
    spider_data.server = server
    spider_data.save()
    return render(request, 'moniter/member-list.html')


def member_first(request):
    return render(request, 'moniter/member-list1.html')


def json_data(request):
    d = {
        "code": 0,
        "msg": "",
        "count": 3000000,
        "data": [
            {
                "id": "10001",
                "username": "杜甫",
                "email": "xianxin@layui.com",
                "sex": "男",
                "city": "浙江杭州",
                "sign": "点击此处，显示更多。当内容超出时，点击单元格会自动显示更多内容。",
                "experience": "116",
                "ip": "192.168.0.8",
                "logins": "108",
                "joinTime": "2016-10-14",
                "dw_xinzhi": {
                    "id": 90,
                    "titel": "小学"
                }
            },
            {
                "id": "10002",
                "username": "李白",
                "email": "xianxin@layui.com",
                "sex": "男",
                "city": "浙江杭州",
                "sign": "君不见，黄河之水天上来，奔流到海不复回。 君不见，高堂明镜悲白发，朝如青丝暮成雪。 人生得意须尽欢，莫使金樽空对月。 天生我材必有用，千金散尽还复来。 烹羊宰牛且为乐，会须一饮三百杯。 岑夫子，丹丘生，将进酒，杯莫停。 与君歌一曲，请君为我倾耳听。(倾耳听 一作：侧耳听) 钟鼓馔玉不足贵，但愿长醉不复醒。(不足贵 一作：何足贵；不复醒 一作：不愿醒/不用醒) 古来圣贤皆寂寞，惟有饮者留其名。(古来 一作：自古；惟 通：唯) 陈王昔时宴平乐，斗酒十千恣欢谑。 主人何为言少钱，径须沽取对君酌。 五花马，千金裘，呼儿将出换美酒，与尔同销万古愁。",
                "experience": "12",
                "ip": "192.168.0.8",
                "logins": "106",
                "joinTime": "2016-10-14",
                "LAY_CHECKED": True,
                "dw_xinzhi": {
                    "id": 90,
                    "titel": "小学"
                }
            },
            {
                "id": "10003",
                "username": "王勃",
                "email": "xianxin@layui.com",
                "sex": "男",
                "city": "浙江杭州",
                "sign": "人生恰似一场修行",
                "experience": "65",
                "ip": "192.168.0.8",
                "logins": "106",
                "joinTime": "2016-10-14",
                "dw_xinzhi": {
                    "id": 90,
                    "titel": "小学"
                }
            },
            {
                "id": "10004",
                "username": "李清照",
                "email": "xianxin@layui.com",
                "sex": "女",
                "city": "浙江杭州",
                "sign": "人生恰似一场修行",
                "experience": "666",
                "ip": "192.168.0.8",
                "logins": "106",
                "joinTime": "2016-10-14",
                "dw_xinzhi": {
                    "id": 90,
                    "titel": "小学"
                }
            },
            {
                "id": "10005",
                "username": "冰心",
                "email": "xianxin@layui.com",
                "sex": "女",
                "city": "浙江杭州",
                "sign": "人生恰似一场修行",
                "experience": "86",
                "ip": "192.168.0.8",
                "logins": "106",
                "joinTime": "2016-10-14",
                "dw_xinzhi": {
                    "id": 90,
                    "titel": "小学"
                }
            },
            {
                "id": "10006",
                "username": "贤心",
                "email": "xianxin@layui.com",
                "sex": "男",
                "city": "浙江杭州",
                "sign": "人生恰似一场修行",
                "experience": "12",
                "ip": "192.168.0.8",
                "logins": "106",
                "joinTime": "2016-10-14",
                "dw_xinzhi": {
                    "id": 90,
                    "titel": "小学"
                }
            },
            {
                "id": "10007",
                "username": "贤心",
                "email": "xianxin@layui.com",
                "sex": "男",
                "city": "浙江杭州",
                "sign": "人生恰似一场修行",
                "experience": "16",
                "ip": "192.168.0.8",
                "logins": "106",
                "joinTime": "2016-10-14",
                "dw_xinzhi": {
                    "id": 90,
                    "titel": "小学"
                }
            },
            {
                "id": "10008",
                "username": "贤心",
                "email": "xianxin@layui.com",
                "sex": "男",
                "city": "浙江杭州",
                "sign": "人生恰似一场修行",
                "experience": "106",
                "ip": "192.168.0.8",
                "logins": "106",
                "joinTime": "2016-10-14",
                "dw_xinzhi": {
                    "id": 90,
                    "titel": "小学"
                }
            },
            {
                "id": "10009",
                "username": "贤心",
                "email": "xianxin@layui.com",
                "sex": "男",
                "city": "浙江杭州",
                "sign": "人生恰似一场修行",
                "experience": "106",
                "ip": "192.168.0.8",
                "logins": "106",
                "joinTime": "2016-10-14",
                "dw_xinzhi": {
                    "id": 90,
                    "titel": "小学"
                }
            },
            {
                "id": "10010",
                "username": "贤心",
                "email": "xianxin@layui.com",
                "sex": "男",
                "city": "浙江杭州",
                "sign": "人生恰似一场修行",
                "experience": "106",
                "ip": "192.168.0.8",
                "logins": "106",
                "joinTime": "2016-10-14",
                "dw_xinzhi": {
                    "id": 90,
                    "titel": "小学"
                }
            }
            # {
            #     "id": "10011",
            #     "username": "贤心",
            #     "email": "xianxin@layui.com",
            #     "sex": "男",
            #     "city": "浙江杭州",
            #     "sign": "人生恰似一场修行",
            #     "experience": "106",
            #     "ip": "192.168.0.8",
            #     "logins": "106",
            #     "joinTime": "2016-10-14",
            #     "dw_xinzhi": {
            #         "id": 90,
            #         "titel": "小学"
            #     }
            # },
            # {
            #     "id": "10012",
            #     "username": "贤心",
            #     "email": "xianxin@layui.com",
            #     "sex": "男",
            #     "city": "浙江杭州",
            #     "sign": "人生恰似一场修行",
            #     "experience": "106",
            #     "ip": "192.168.0.8",
            #     "logins": "106",
            #     "joinTime": "2016-10-14",
            #     "dw_xinzhi": {
            #         "id": 90,
            #         "titel": "小学"
            #     }
            # },
            # {
            #     "id": "10013",
            #     "username": "贤心",
            #     "email": "xianxin@layui.com",
            #     "sex": "男",
            #     "city": "浙江杭州",
            #     "sign": "人生恰似一场修行",
            #     "experience": "106",
            #     "ip": "192.168.0.8",
            #     "logins": "106",
            #     "joinTime": "2016-10-14",
            #     "dw_xinzhi": {
            #         "id": 90,
            #         "titel": "小学"
            #     }
            # },
            # {
            #     "id": "10014",
            #     "username": "贤心",
            #     "email": "xianxin@layui.com",
            #     "sex": "男",
            #     "city": "浙江杭州",
            #     "sign": "人生恰似一场修行",
            #     "experience": "106",
            #     "ip": "192.168.0.8",
            #     "logins": "106",
            #     "joinTime": "2016-10-14",
            #     "dw_xinzhi": {
            #         "id": 90,
            #         "titel": "小学"
            #     }
            # },
            # {
            #     "id": "10015",
            #     "username": "贤心",
            #     "email": "xianxin@layui.com",
            #     "sex": "男",
            #     "city": "浙江杭州",
            #     "sign": "人生恰似一场修行",
            #     "experience": "106",
            #     "ip": "192.168.0.8",
            #     "logins": "106",
            #     "joinTime": "2016-10-14",
            #     "dw_xinzhi": {
            #         "id": 90,
            #         "titel": "小学"
            #     }
            # },
            # {
            #     "id": "10016",
            #     "username": "贤心",
            #     "email": "xianxin@layui.com",
            #     "sex": "男",
            #     "city": "浙江杭州",
            #     "sign": "人生恰似一场修行",
            #     "experience": "106",
            #     "ip": "192.168.0.8",
            #     "logins": "106",
            #     "joinTime": "2016-10-14",
            #     "dw_xinzhi": {
            #         "id": 90,
            #         "titel": "小学"
            #     }
            # },
            # {
            #     "id": "10017",
            #     "username": "贤心",
            #     "email": "xianxin@layui.com",
            #     "sex": "男",
            #     "city": "浙江杭州",
            #     "sign": "人生恰似一场修行",
            #     "experience": "106",
            #     "ip": "192.168.0.8",
            #     "logins": "106",
            #     "joinTime": "2016-10-14",
            #     "dw_xinzhi": {
            #         "id": 90,
            #         "titel": "小学"
            #     }
            # },
            # {
            #     "id": "10018",
            #     "username": "贤心",
            #     "email": "xianxin@layui.com",
            #     "sex": "男",
            #     "city": "浙江杭州",
            #     "sign": "人生恰似一场修行",
            #     "experience": "106",
            #     "ip": "192.168.0.8",
            #     "logins": "106",
            #     "joinTime": "2016-10-14",
            #     "dw_xinzhi": {
            #         "id": 90,
            #         "titel": "小学"
            #     }
            # },
            # {
            #     "id": "10019",
            #     "username": "贤心",
            #     "email": "xianxin@layui.com",
            #     "sex": "男",
            #     "city": "浙江杭州",
            #     "sign": "人生恰似一场修行",
            #     "experience": "106",
            #     "ip": "192.168.0.8",
            #     "logins": "106",
            #     "joinTime": "2016-10-14",
            #     "dw_xinzhi": {
            #         "id": 90,
            #         "titel": "小学"
            #     }
            # },
            # {
            #     "id": "10020",
            #     "username": "贤心",
            #     "email": "xianxin@layui.com",
            #     "sex": "男",
            #     "city": "浙江杭州",
            #     "sign": "人生恰似一场修行",
            #     "experience": "106",
            #     "ip": "192.168.0.8",
            #     "logins": "106",
            #     "joinTime": "2016-10-14",
            #     "dw_xinzhi": {
            #         "id": 90,
            #         "titel": "小学"
            #     }
            # }
        ]}
    return JsonResponse(d)


def spiders_json(request, project_id):
    import sys
    # path = os.getcwd() + '\project_filed\{project_name}\{project_name_1}\spiders'.format(project_name=project.project_name,project_name_1=project.project_name)
    # sys.path.append(path)
    # pathDir = os.listdir(path)
    # for k, fileName in enumerate(pathDir):
    #     if (fileName) and ('__' not in fileName):
    #         frame = __import__(fileName.replace('.py', ''))
    #         classname = getattr(frame, dir(frame)[0])

    a = {"code": 0, "msg": "", "count": 1000, "data": []}
    html = """
          <a class="layui-btn layui-btn-xs" lay-event="detail">查看</a>
          <a class="layui-btn layui-btn-xs" lay-event="edit" onclick="xadmin.open('&nbsp;&nbsp;编辑','/edit_spider/{spider_id}/{projectname}',800,600)">编辑</a>
          <a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="del"  onclick="xadmin.open('&nbsp;&nbsp;信息','/spider_del_info/{spider_id}',250,180)">删除</a>"""
    if project_id != '999999999999':
        project = models.creat_project_lists.objects.filter(pk=project_id)[0]
        all_spider = models.creat_spider_lists.objects.filter(projectname=project.project_name)
        for i in all_spider:
            a['data'].append({"id": i.id, "spidername": i.spidername, "islong": i.islong, "nextstatus": i.laststatus,
                              "lasttime": i.lasttime, "creattime": i.creattime, "remarks": i.spiderdesc,
                              'operation': html.format(spider_id=i.id, projectname=project.project_name)})
    elif project_id == '999999999999':
        all_spider = models.creat_spider_lists.objects.all()
        print(all_spider)
        for i in all_spider:
            a['data'].append({"id": i.id, "spidername": i.spidername, "islong": i.islong, "nextstatus": i.laststatus,
                              "lasttime": i.lasttime, "creattime": i.creattime, "remarks": i.spiderdesc,
                              'operation': html.format(spider_id=i.id, projectname=i.projectname)})
    return JsonResponse(a)

def runner(request, project_name, spider_name):
    a = """from scrapy.cmdline import execute
execute(['scrapy', 'crawl', '{spider_name}'])  # 执行一个
"""
    file_path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}\\run.py'.format(projectname=project_name, projectname_1=project_name)
    with open(file_path, 'wb') as file:
        file.write(a.format(spider_name=spider_name).encode('utf-8'))
    path = os.getcwd() + '\project_filed\{projectname}\{projectname_1}'.format(projectname=project_name, projectname_1=project_name)
    # print('cd {path} & set pa=%cd% & echo %pa% & python run.py'.format(path=path))
    os.system('cd {path} & python run.py'.format(path=path))
    return render(request, 'moniter/spider_info.html', {'project_name': project_name, 'spider_name': spider_name})

def stoped(request, project_name, spider_name):
    pass