import hashlib
from django.shortcuts import render, redirect, reverse
from .models import User
from .forms import UserForm, RegisterForm

def index(request):
    pass
    return render(request, 'index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = '所有字段必须填写'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect(reverse('index')) # 如果密码和用户名都正确, 则跳转到主页
                else:
                    message = '密码不正确!'
            except:
                message = '用户名不存在!'
        return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = '请检查输入的内容!'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']

            if password1 != password2:
                message = '请重新输入, 两次输入的密码不一致!'
                return render(request, 'register.html', locals())
            else:
                same_email = User.objects.filter(email=email)
                if same_email:
                    message = '请重新输入, 邮箱已经被注册过了!'
                    return render(request, 'register.html', locals())
                same_username = User.objects.filter(name=username)
                if same_username:
                    return render(request, 'register.html', locals())

                new_user = User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect(reverse('login'))
    register_form = RegisterForm()
    return render(request, 'register.html', locals())



def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()
    return redirect('index')

def hash_code(s, water='water'):
    h = hashlib.sha256()
    s += water
    h.update(s.encode())
    return h.hexdigest()