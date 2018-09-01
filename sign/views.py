from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from sign.models import Guest, Event

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




