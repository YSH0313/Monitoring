from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from . import models
from django.core.paginator import Paginator
import datetime
import hashlib
import arrow
import time
import json
import collections


# Create your views here.
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

def login(request):
    username_login = request.POST.get('username')
    password_login = request.POST.get('password')
    try:
        username = models.user.objects.filter(username=username_login)
        password = models.user.objects.filter(password=password_login)
        if hashlib.md5((password_login+password_login+'qaz').encode(encoding='UTF-8')).hexdigest() == password:
            if request.method == 'GET':
                request.session['username'] = username
                return render(request, 'moniter/index.html', {'username': request.session['username']})
        else:
            return render(request, 'moniter/login.html')
    except:
        return render(request, 'moniter/login.html')


def index(request):
    return render(request, 'moniter/index.html')


def reg_user(request):
    if request.method == 'GET':
        return render(request, 'moniter/registered.html')
    else:
        username = request.POST.get('username')
        password = hashlib.md5((request.POST.get('username')+request.POST.get('confirm_password')+'qaz').encode(encoding='UTF-8')).hexdigest()
        email = request.POST.get('email')
        models.user.objects.create(username=username, password=password, email=email)
        return render(request, 'moniter/login.html')



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
        one = models.data_count.objects.get(time_date=getYesterday(0), dimensions='裁判文书').count
        two = models.data_count.objects.get(time_date=getYesterday(1), dimensions='裁判文书').count
        three = models.data_count.objects.get(time_date=getYesterday(2), dimensions='裁判文书').count
        four = models.data_count.objects.get(time_date=getYesterday(3), dimensions='裁判文书').count
        five = models.data_count.objects.get(time_date=getYesterday(4), dimensions='裁判文书').count
        six = models.data_count.objects.get(time_date=getYesterday(5), dimensions='裁判文书').count
        seven = models.data_count.objects.get(time_date=getYesterday(6), dimensions='裁判文书').count
        eight = models.data_count.objects.get(time_date=getYesterday(7), dimensions='裁判文书').count

        new_num['one_num'] = one
        new_num['two_num'] = two
        new_num['three_num'] = three
        new_num['four_num'] = four
        new_num['five_num'] = five
        new_num['six_num'] = six
        new_num['seven_num'] = seven

        new_num['seven'] = seven-eight
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

        one_month_num = models.month_datacount.objects.get(time_date=getMonth(6), dimensions='裁判文书').count
        two_month_num = models.month_datacount.objects.get(time_date=getMonth(5), dimensions='裁判文书').count
        three_month_num = models.month_datacount.objects.get(time_date=getMonth(4), dimensions='裁判文书').count
        four_month_num = models.month_datacount.objects.get(time_date=getMonth(3), dimensions='裁判文书').count
        five_month_num = models.month_datacount.objects.get(time_date=getMonth(2), dimensions='裁判文书').count
        six_month_num = models.month_datacount.objects.get(time_date=getMonth(1), dimensions='裁判文书').count
        seven_month_num = models.month_datacount.objects.get(time_date=getMonth(0), dimensions='裁判文书').count

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

        return render(request, 'moniter/welcome1.html', {'new_num': new_num, 'dimensions': dimensions, 'important_all': important_all})

    elif request.method == 'POST':
        num = {}
        new_num = {}
        dimensions = request.POST.get('dimensions')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        type_check = request.POST.get('month')

        if type_check != 'month':
            one_month_num = models.month_datacount.objects.get(time_date=getMonth(6), dimensions='裁判文书').count
            two_month_num = models.month_datacount.objects.get(time_date=getMonth(5), dimensions='裁判文书').count
            three_month_num = models.month_datacount.objects.get(time_date=getMonth(4), dimensions='裁判文书').count
            four_month_num = models.month_datacount.objects.get(time_date=getMonth(3), dimensions='裁判文书').count
            five_month_num = models.month_datacount.objects.get(time_date=getMonth(2), dimensions='裁判文书').count
            six_month_num = models.month_datacount.objects.get(time_date=getMonth(1), dimensions='裁判文书').count
            seven_month_num = models.month_datacount.objects.get(time_date=getMonth(0), dimensions='裁判文书').count

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


            start_year = int(startdate[:4])
            start_month = int(startdate[5:7].replace('0', ''))
            start_day = int(startdate[8:10].replace('0', ''))
            end_month = int(enddate[5:7].replace('0', ''))
            end_day = int(enddate[8:10].replace('0', ''))
            # print(start_year, start_month, start_day, end_month, end_day)
            for d in range(start_year, start_year+1):
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
            dimensions['dimensions'] = dimensions_lists

            info = {'staartdate': startdate, 'endate': enddate, 'dimensions_name': dimensions}
            return render(request, 'moniter/welcome1.html', {'new_num': new_num, 'dimensions': dimensions_map, 'info': info, 'important_all': important_all})

        elif type_check == 'month':
            one = models.data_count.objects.get(time_date=getYesterday(0), dimensions='裁判文书').count
            two = models.data_count.objects.get(time_date=getYesterday(1), dimensions='裁判文书').count
            three = models.data_count.objects.get(time_date=getYesterday(2), dimensions='裁判文书').count
            four = models.data_count.objects.get(time_date=getYesterday(3), dimensions='裁判文书').count
            five = models.data_count.objects.get(time_date=getYesterday(4), dimensions='裁判文书').count
            six = models.data_count.objects.get(time_date=getYesterday(5), dimensions='裁判文书').count
            seven = models.data_count.objects.get(time_date=getYesterday(6), dimensions='裁判文书').count
            eight = models.data_count.objects.get(time_date=getYesterday(7), dimensions='裁判文书').count

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
                for k, m in enumerate(range(start_month, end_month+1)):
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
                start_month = start_month-1
                if start_month < 10:
                    time_date = str(start_year)+"-0"+str(start_month)
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
                          {'new_num': new_num, 'dimensions': dimensions_map, 'infos': infos, 'important_all': important_all})


def order(request):
    return render(request, 'moniter/order-list.html')


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
