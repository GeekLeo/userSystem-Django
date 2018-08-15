import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'userSystem.settings'

if __name__ == '__main__':

    subject, from_email, to = '来自userSystem的测试邮件', 'geek_leo@sina.com', ['geek_leo@outlook.com', '747430227@qq.com']
    text_content = '欢迎注册本网站'
    html_content = '<p>Welcome to visit <a href="http://www.google.com" target=blank>our site</a>, enjoy your time!</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
