from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render,get_object_or_404
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Read, Guest

# Create your views here.

def index(request):
    #return HttpResponse("hello,admin")
    return render(request, "index.html")
'''
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if username == 'admin' and password == 'admin123':
            #return HttpResponse('login success!')
            #return HttpResponseRedirect('/read_plan/')
            response = HttpResponseRedirect('/read_plan/')
            #response.set_cookie('user',username,3600)  #添加浏览器cookie
            request.session['user'] = username  #将session信息记录到浏览器
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})
'''
#@login_required
def login_action(request):
    if request.method =='POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        #使用Django认证登录
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username   #将session信息记录到浏览器
            response = HttpResponseRedirect('/read_plan/')
            return  response
        else:
            return render(request, 'index.html', {'error':'username or password is error!'})
#读书计划列表
@login_required
def read_plan(request):
    read_list = Read.objects.all()# 获取读书计划信息
    #增加分页器
    paginator = Paginator(read_list,2)
    page = request.GET.get('page')
    try:
        counts = paginator.page(page)
    except PageNotAnInteger:
        counts = paginator.page(1)
    except EmptyPage:
        counts = paginator.page(paginator.num_pages)
    #username = request.COOKIES.get('user','')  #读取浏览器cookie
    username = request.session.get('user','')  #读取浏览器session
    return render(request,"read_plan.html",{"user":username,"readplans":counts})

#读书计划姓名搜索
@login_required
def search_name(request):
    username = request.session.get('user','')
    #通过GET方法获取name关键字
    search_name = request.GET.get('name','')

    #在Read中匹配name字段
    readplan_list = Read.objects.filter(name__contains=search_name)
    #分页器
    paginator = Paginator(readplan_list,2)
    page = request.GET.get('page')
    try:
        counts = paginator.page(page)
    except PageNotAnInteger:
        counts = paginator.page(1)
    except EmptyPage:
        counts = paginator.page(paginator.num_pages)
    #将匹配到的读书会列表注意这里是列表不是，返回给客户端
    #这里最重要，为了实现分页器功能，我们增加了一个返回值，即search_realname，也就是指定过滤的用户名称，并将这个值和readplans一起传递给guest_manage.html
    return render(request,'read_plan.html', {"user":username,"readplans":counts, "search_name":search_name})
#用户管理列表
@login_required
def guest_manage(request):
    username = request.session.get('user','')
    guest_list = Guest.objects.all()## 通过Guest.objects.all获取全部用户对象
    #增加分页器
    paginator = Paginator(guest_list,2)# 把查询出来的所有用户列表guest_list放到Paginator类中，划分每页显示2条数据
    page = request.GET.get('page')  #通过GET请求得到当前要显示第几页的数据
    try:
        contacts = paginator.page(page) #获取第page页的数据
    except PageNotAnInteger:
        contacts = paginator.page(1)  # 如果page不是整数，取第一页面数据
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages) # 如果page不在范围内，取最后一页面数据
    return render(request, "guest_manage.html", {"user":username,"guests":contacts})
    # 通过render()方法附加在guest_manage.html页面返回给客户端

#用户搜索
@login_required
def search_guest(request):
    username = request.session.get('user','')
    search_wdnum = request.GET.get('wd_num','')
    guest_list = Guest.objects.filter(wd_num__contains=search_wdnum)
    return render(request,'guest_manage.html', {"user":username,"guests":guest_list})

#新增读书计划
@login_required
def add_index(request):
    #get_object_or_404()方法：默认调用Django的table.objects.get()方法，如果查询的对象不存在，
    # 则会抛出一个HTTP 404异常，这样就省去了对table.objects.get()方法做异常断言。
    #read = get_object_or_404(Read)
    read = Read.objects.all()
    return render(request, "add_index.html", {"read":read})

#新增信息动作
@login_required
def add_index_action(request):
    #list = get_object_or_404(Read)  # 还是利用get_object_or_404()方法获取对应读书，没有就报404异常
    if request.method == 'GET':
        return render(request,'add_index.html')
    elif request.method =='POST':
        read = Read()
        read.wd_num = request.POST.get('wd_num')
        read.name = request.POST.get('name')
        read.group_name = request.POST.get('group_name')
        read.book_name = request.POST.get('book_name')
        read.target = request.POST.get('target')
        read.save()
    return render(request,'read_plan.html')

#读书列表编辑页面
@login_required
def update_index(request,rid):
    reads = get_object_or_404(Read, id=rid)
    #reads = request.POST.get()
    return render(request, "update_index.html", {"reads":reads})
#编辑功能提交动作
@login_required
def update_index_action(request,rid):
    # 还是利用get_object_or_404()方法通过eid获取对应发布会，没有就报404异常
    read = get_object_or_404(Read, id=rid)
    read.operation = request.POST.get('operation')
    read.pay_type = request.POST.get('pay_type')
    read.save()
    return render(request,'read_plan.html')

#退出系统
@login_required
def logout(request):
    auth.logout(request) #diango 的auth.logout()方法用于退出系统，它可以清除浏览器保存的用户信息，这样用户就不用考虑如何删除浏览器的cookie信息
    response = HttpResponseRedirect('/index/')
    return response


    '''
    if request.method == 'GET':
        return render(request,'add_index.html')
    elif request.method =='POST':
        read = Read()
        read.wd_num = request.POST.get('wd_num')
        read.name = request.POST.get('name')
        read.group_name = request.POST.get('group_name')
        read.book_name = request.POST.get('book_name')
        read.target = request.POST.get('target')
        read.save()
    return render(request,'read_plan.html')
    '''
    '''
    phone = request.POST.get('phone', '')# 利用request的POST请求获取用户输入的手机号
    result = Guest.objects.filter(phone=phone)                 # 根据用户输入的手机号查询在Guest表中的记录
    if not result:                                             # 如果用户输入的手机号在Guest表不存在，则提示用户“phone error.”
        return render(request, 'sign_index.html', {'list': list, 'hint': 'phone error.'})
    '''
