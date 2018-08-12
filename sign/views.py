from django.shortcuts import render
from django.http import HttpResponse

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

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == 'admin' and password == 'admin':
            return HttpResponse('login success!')
        else:
            return render(request, 'login1.html', {'error': 'username or password error!'})


