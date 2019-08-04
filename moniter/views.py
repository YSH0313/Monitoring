from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from . import models
from django.core.paginator import Paginator
import datetime
import hashlib


# Create your views here.
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
    # count = models.app_num.objects.count()
    new_num = {}
    num = models.data_count.objects.get(pk=1)
    new_num['monday'] = num.monday
    new_num['tuesday'] = num.tuesday - num.monday
    new_num['wednesday'] = num.wednesday - num.tuesday
    new_num['thursday'] = num.thursday - num.wednesday

    def getYesterday(num):
        today = datetime.date.today()
        twoday = datetime.timedelta(days=num)
        yesterday = today - twoday
        return str(yesterday)

    new_num['four_day'] = getYesterday(3)
    new_num['five_day'] = getYesterday(2)
    new_num['six_day'] = getYesterday(1)
    new_num['now'] = getYesterday(0)

    data_base = {}

    data_base['data_base'] = [
        'data_base1',
        'data_base2',
        'data_base3',
        'qaz',
        'moniter_app_num',
    ]

    return render(request, 'moniter/welcome1.html', {'new_num': new_num, 'data_base': data_base})


def edit_selectbase(request):
    new_num = {}
    num = models.data_count.objects.get(pk=1)
    new_num['monday'] = num.monday
    new_num['tuesday'] = num.tuesday - num.monday
    new_num['wednesday'] = num.wednesday - num.tuesday
    new_num['thursday'] = num.thursday - num.wednesday

    def getYesterday(num):
        today = datetime.date.today()
        twoday = datetime.timedelta(days=num)
        yesterday = today - twoday
        return str(yesterday)

    new_num['four_day'] = getYesterday(3)
    new_num['five_day'] = getYesterday(2)
    new_num['six_day'] = getYesterday(1)
    new_num['now'] = getYesterday(0)

    data_base = {}

    data_base['data_base'] = [
        'data_base1',
        'data_base2',
        'data_base3',
        'qaz',
        'moniter_app_num',
    ]

    database_name = request.POST.get('data_base')
    print(database_name)
    data = models.data_count.objects.filter(database_name=database_name)[0]
    print(data.monday, data.tuesday, data.wednesday, data.thursday)
    new_num['monday'] = data.monday
    new_num['tuesday'] = data.tuesday - data.monday
    new_num['wednesday'] = data.wednesday - data.tuesday
    new_num['thursday'] = data.thursday - data.wednesday

    return render(request, 'moniter/welcome1.html',
                  {'new_num': new_num, 'data_base': data_base, 'database_name': database_name})


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
    paginator = Paginator(all_spider, 2)
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
        '机器1',
        '机器2',
        '机器3',
        '机器4',
        '机器5',
    ]
    data['interval_time'] = spider_data.interval_time
    data['data_base'] = spider_data.data_base
    data['server'] = data['servers'][0]
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
            }
        ]}
    return JsonResponse(d)
