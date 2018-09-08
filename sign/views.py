from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from sign.models import Guest, Event
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sign.forms import AddEventForm, AddGuestForm

# Create your views here.

# 首页方法
def index(request):
    if request.method == 'GET':
        name = request.GET.get("name")
        if name == None:
            return HttpResponse('hello world')
        else:
            return HttpResponse('hello, '+ name)


# 登录方法
def login(request):
    return render(request, 'login1.html')


# 登录动作的处理
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login1.html', {'error': '用户名或密码错误'})
        else:
            auth.login(request, user)
            response = HttpResponseRedirect('/event_manage/')
            # 将cookie数据存入浏览器
            # response.set_cookie('username', username, 3600)

            # 将 session 信息记录到浏览器
            request.session['user'] = username
            return response
            # return HttpResponseRedirect('event_manage.html')

        # if username == 'admin' and password == 'admin':
        #     response = HttpResponseRedirect('/event_manage/')
        #     # 将cookie数据存入浏览器
        #     # response.set_cookie('username', username, 3600)
        #
        #     # 将 session 信息记录到浏览器
        #     request.session['user'] = username
        #     return response
        #     # return HttpResponseRedirect('event_manage.html')
        # elif username == '' or password == '':
        #     return render(request, 'login1.html', {'error': '用户名或密码不能为空'})
        # elif username != 'admin' or password != 'admin':
        #     return render(request, 'login1.html', {'error': '用户名或密码错误'})

    else:
        return render(request, 'login1.html')


# 发布会列表
@login_required
def event_manage(request):
    # 将cookie数据从浏览器中取出
    # user_cookie = request.COOKIES.get('username', '')

    # 读取浏览器 session
    user_session = request.session.get('user', '')
    # 增加发布会查询
    event_list = Event.objects.all()
    print(event_list)

    return render(request, 'event_manage.html', {'user':user_session, 'events':event_list})


# 添加发布会
def add_event(request):
    # 读取浏览器 session
    user_session = request.session.get('user', '')

    if request.method == 'POST':
        form = AddEventForm(request.POST) # form 包含提交的数据
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            limit = form.cleaned_data['limit']
            start_time = form.cleaned_data['start_time']
            status = form.cleaned_data['status']
            if status is True:
                status = 1
            else:
                status = 0

            Event.objects.create(name=name,limit=limit,address=address,status=status,start_time=start_time)
            return render(request, "add_event.html", {"user": user_session, "form": form, "success": "添加发布会成功!"})

    else:
        form = AddEventForm()

    return render(request, "add_event.html", {"user": user_session, "form": form})



# 嘉宾列表
@login_required
def guest_manage(request):
    # 读取浏览器 session
    user_session = request.session.get('user', '')
    guests = Guest.objects.all()    # 查询所有存在的嘉宾
    # print(guests)
    paginator = Paginator(guests, 2)    # 分页器，每页显示两条记录

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整型，或为None，取第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user":user_session, "guest":contacts})



# 添加嘉宾
def add_guest(request):
    # 读取浏览器 session
    user_session = request.session.get('user', '')

    if request.method == 'POST':
        form = AddGuestForm(request.POST)

        if form.is_valid():
            event = form.cleaned_data['event']
            realname = form.cleaned_data['realname']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            sign = form.cleaned_data['sign']
            if sign is True:
                sign = 1
            else:
                sign = 0

            Guest.objects.create(event=event,realname=realname,phone=phone,email=email,sign=sign)
            return render(request, "add_guest.html", {"user": user_session, "form": form, "success": "添加嘉宾成功!"})

    else:
        form = AddGuestForm()

    return render(request, "add_guest.html", {"user": user_session, "form": form})



# 通过手机号码查询嘉宾列表
@login_required
def search_phone(request):
    user_session = request.session.get('user', '')
    search_phone = request.GET.get('phone', "")
    # 通过手机号码模糊查询
    guest = Guest.objects.filter(phone__contains=search_phone)

    if len(guest) == 0:
        return render(request, "guest_manage.html", {"user":user_session,
                                                     "hint":"根据输入的手机号码查询结果为空！"})
    paginator = Paginator(guest, 2)    # 分页器，每页显示两条记录

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整型，或为None，取第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user":user_session,
                                                 "guest":contacts,
                                                 "phone":search_phone})

# 签到页面
# @login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)
    # 签到人数
    guest_data = str(len(guest_list))
    # 已签到人数
    sign_data = 0
    for guest in guest_list:
        if guest.sign == True:
            sign_data += 1
    return render(request, "sign_index.html", {'event':event,
                                             'guest':guest_data,
                                             'sign':sign_data})


# 签到动作
@login_required
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)
    guest_data = str(len(guest_list))
    sign_data = 0
    for guest in guest_list:
        if guest.sign == True:
            sign_data += 1

    phone =  request.POST.get('phone','')

    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'phone error.','guest':guest_data,'sign':sign_data})

    result = Guest.objects.filter(phone = phone,event_id = event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.','guest':guest_data,'sign':sign_data})

    result = Guest.objects.get(event_id = event_id,phone = phone)

    if result.sign:
        return render(request, 'sign_index.html', {'event': event,'hint': "用户已签到，请勿重复签到！",'guest':guest_data,'sign':sign_data})
    else:
        Guest.objects.filter(event_id = event_id,phone = phone).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,'hint':'签到成功!',
                                                   'user': result,
                                                   'guest':guest_data,
                                                   'sign':str(int(sign_data)+1)
                                                   })

# 退出登录
@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/logout/')
    return response











