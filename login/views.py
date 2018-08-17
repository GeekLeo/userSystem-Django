from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
import datetime
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone


# Create your views here.

def hash_code(s, salt='userSystem'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code


def send_email(email, code):
    subject = '来自userSystem的注册确认邮件'

    text_content = '''感谢注册userSystem，enjoy your time ！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>userSystem</a>，\
                    enjoy your time ！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_reset_email(email, code):
    subject = '来自userSystem的重置密码邮件'

    text_content = '''重置密码需要你的邮箱服务器提供HTML链接功能 ！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>请点击以下链接进行密码重置！</p>
                    <p><a href="http://{}/reset_password/?code={}&email={}" target=blank>重置密码</a></p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, email, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect("index")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = 'All field are required'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if not user.has_confirmed:
                    message = '该用户还未通过邮件确认！'
                    return render(request, 'login/login.html', locals())
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('index')
                else:
                    message = 'wrong password'
            except:
                message = '用户名不存在'
        return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('index')
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "Please check the field"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = "两次输入密码不相同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = "用户名已存在，请重新选择用户名！"
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = "该邮箱地址已被注册，请更换其他邮箱！"
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)
                message = '请前往注册邮箱，进行邮件确认！'

                return render(request, 'login/confirm.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("index")
    request.session.flush()
    return redirect("index")


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = timezone.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())


def change_password(request):
    if not request.session.get('is_login', None):
        return redirect("index")
    if request.method == "POST":
        change_password_form = forms.ChangePasswordForm(request.POST)
        message = "请检查字段"
        if change_password_form.is_valid():
            old_password = change_password_form.cleaned_data['old_password']
            new_password1 = change_password_form.cleaned_data['new_password1']
            new_password2 = change_password_form.cleaned_data['new_password2']
            if new_password1 != new_password2:
                message = "两次输入密码不相同！"
                return render(request, 'login/changepassword.html', locals())
            else:
                user = models.User.objects.get(name=request.session['user_name'])
                if user.password == hash_code(old_password):
                    user.password = hash_code(new_password1)
                    user.save()
                    message = 'The password has been changed'
                    return render(request, 'login/changepassword.html', locals())
                else:
                    message = 'Wrong password'
        return render(request, 'login/changepassword.html', locals())
    change_password_form = forms.ChangePasswordForm()
    return render(request, 'login/changepassword.html', locals())


def apply_reset(request):
    if request.method == "POST":
        apply_reset_form = forms.ApplyResetForm(request.POST)
        message = "请检查字段"
        if apply_reset_form.is_valid():
            email = apply_reset_form.cleaned_data['email']
            try:
                user = models.User.objects.get(email=email)
                code = make_confirm_string(user)
                send_reset_email(email, code)
                message = '请前往邮箱，进行密码重置！'
            except:
                message = "该邮箱未注册本网站账号"
        return render(request, 'login/applyreset.html', locals())
    apply_reset_form = forms.ApplyResetForm()
    return render(request, 'login/applyreset.html', locals())


def reset_password(request):
    code = request.GET.get('code', None)
    email = request.GET.get('email', None)

    message = ''
    try:
        reset_password_confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的重置密码请求!'
        return render(request, 'login/confirm.html', locals())
    c_time = reset_password_confirm.c_time
    now = timezone.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        reset_password_confirm.delete()
        message = '您的邮件已经过期！请重新提交忘记密码申请!'
        return render(request, 'login/applyreset.html', locals())
    else:
        # reset_password_form = forms.ResetPasswordForm()
        # return render(request, 'login/resetpassword.html', locals())
        return redirect('reset_confirm')


def reset_confirm(request):
    if request.method == "POST":
        reset_password_form = forms.ResetPasswordForm(request.POST)
        message = "请检查字段"
        if reset_password_form.is_valid():
            email = reset_password_form.cleaned_data['email']
            new_password1 = reset_password_form.cleaned_data['new_password1']
            new_password2 = reset_password_form.cleaned_data['new_password2']
            if new_password1 != new_password2:
                message = "两次输入密码不相同！"
                return render(request, 'login/resetpassword.html', locals())
            else:
                try:
                    user = models.User.objects.get(email=email)
                    user.password = hash_code(new_password1)
                    user.save()
                    message = "密码已重置，请登陆！"
                    user.confirmstring.delete()

                except:
                    message = "该邮箱未注册本网站账号"
        return render(request, 'login/confirm.html', locals())
    reset_password_form = forms.ResetPasswordForm()
    return render(request, 'login/resetpassword.html', locals())
