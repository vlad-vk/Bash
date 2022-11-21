# coding=utf8; version=2013011202

#-------------------------------------------------------------------------------
# 1)
# В apache2 подключается модуль mod_python и в конфигурации указывается
# имя проекта python (vvkws) и путь к каталогу проектов (/bm/py):
# <Location "/">
#    SetHandler python-program
#    PythonHandler django.core.handlers.modpython
#    SetEnv DJANGO_SETTINGS_MODULE vvkws.settings
#    PythonPath "['/bm/py'] + sys.path"
# </Location>

# 2)
# В каталоге по пути /bm/py создать проект (выполнить в shell-е):
# django-admin startproject vvkws
# При этом создаётся каталог /bm/py/vvkws и в нём файлы: 
# __init__.py, manage.py, settings.py, urls.py
# __init__.py  - пустой файл, который нужен python-у (для идентификации пакета)
# manager.py   - django-manager (http сервер для отладки, shell и другое...)
# settings.py  - файл настроек проекта (БД, пути, каталоги, админка)
# urls.py      - файл сопоставления путей сайта(проекта) и функций им соответствующих

# 3)
# Нижеприведённый в комментарии код - это файл urls.py, на который указывает ссылка
# в settings.py : ROOT_URLCONF = 'vvkws.urls'  # vvkws - имя проекта, urls - имя файла (urls.py)
#from django.conf.urls.defaults import patterns, include, url
#from vvkws.views import *
#urlpatterns = patterns('',
#    ('^hello/$',hello),
#    ('^time/$',nowtm),
#    ('^now/1/$',nowtpls1),
#    ('^now/2/$',nowtpls2),
#    (r'^time/plus/(\d{1,2})/$',hour_ahead),
#    (r'^time/tpls/(\d{1,2})/$',hour_ahead_tpls1),
#    ('^hosts/$',host_list),
#)

# 4)
# Имя данного файла (views.py) указывается в urls.py, в строке: from vvkws.views import
# Данный файл создаётся вручную и в нём определяются функции, которые указываются
# в файле urls.py для связи путей сайта.

# 5)
# В файле settings.py определяем:
# import os # можно включить, если планируем использовать какие-то переменный системы
# TIME_ZONE = 'Europe/Kiev'   # Временная зона
# TEMPLATE_DIRS = (           # Каталоги, где будут находится файлы шаблонов (templates)
#    '/bm/py/vvkws/tpls',
# )
# Файлы шаблонов создаются в ручную, имена и расширения выбираются разработчиком

# 6)
# Ниже приведены примеры и пробы по книге: Django - Подробное руководство. А.Головатый,Д.Карлан-Мосс
# Вывод функций осуществляется через WEB-сервер (Например, manager.py)


#-------------------------------------------------------------------------------
from django import forms
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context
from django.template.loader import get_template
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
import datetime
import MySQLdb
import reportlab
#from vvkws.models import Event, BlogEntry


# Вывод текста: Hello world !
def hello (request):
    return(HttpResponse('Hello world !'))
def ehllo (request):
    return(HttpResponse('Ehllo world !'))

# Вывод текущего времени
def nowtm (request):
    curtime=datetime.datetime.now()
    html="<html><body>Сейчас: %s</body><html>" % (curtime)
    return(HttpResponse(html))

# Тот же самый вывод через template(шаблон) curdt.htm (с родительским наследием basedt.htm)
def nowtpls1(request):
    curtime=datetime.datetime.now()
    tpls=get_template('curdt.htm')
    html=tpls.render(Context({'current_time':curtime}))
    return(HttpResponse(html))

# Тоже самое более компактным способом
def nowtpls2(request):
    curtime=datetime.datetime.now()
    return render_to_response('curdt.htm',{'current_time':curtime})

# Вывод времени со смещением по часам от +0 до 99. При другом смещении - HTTP404
def hour_ahead (request, offset):
    try:
        offset=int(offset)
    except ValueError:
        raise Http404()
    dt=datetime.datetime.now()+datetime.timedelta(hours=offset) 
#   assert False  # принудительный останов программы для отладки (раскоментировать)
    html="<html><body>Через %d час будет %s .</body><html>" % (offset,dt)
    return(HttpResponse(html))

# Тоже самое по шаблону hour_ahead.htm
def hour_ahead_tpls1 (request, offset):
    try:
        hour_offset=int(offset)
    except ValueError:
        raise Http404()
    next_time=datetime.datetime.now()+datetime.timedelta(hours=hour_offset)
    return render_to_response('hour_ahead.htm',{ 'hour_offset':hour_offset,'next_time':next_time})

# Вывод из БД в шаблон host_list.htm (с родительским наследием basedt.htm)
def host_list(request):
    db = MySQLdb.connect(user='root',db='mysql',passwd='', host='localhost')
    cursor = db.cursor()
    cursor.execute('SELECT host,user FROM user ORDER BY host')
    resrow=[];
    for row in cursor.fetchall(): resrow.append(row);
    db.close()
    return render_to_response('host_list.htm', {'resrow':resrow})

#-------------------------------------------------------------------------------
# 7)
# Создаём приложение: ./manage.py startapp books
# Создаём модели(описание таблиц и типов) для базы данных в /bm/py/vvkws/books/models.py:
# from django.db import models
# class Publisher(models.Model):
#    name = models.CharField(max_length=30)
#    address = models.CharField(max_length=50)
#    city = models.CharField(max_length=60)
#    state_province = models.CharField(max_length=30)
#    country = models.CharField(max_length=50)
#    website = models.URLField()
# class Author(models.Model):
#    first_name = models.CharField(max_length=30)
#    last_name = models.CharField(max_length=40)
#    email = models.EmailField()
# class Book(models.Model):
#    title = models.CharField(max_length=100)
#    authors = models.ManyToManyField(Author)
#    publisher = models.ForeignKey(Publisher)
#    publication_date = models.DateField()
#
# Из моделей просматриваем команды создания таблиц в БД: manage.py sqlall books
# Если всё правильно, создаём таблицы в БД: manage.py syncdb
# Если БД уже создана, получить модель можно следующей командой: manage.py inspectdb

# 8)
# В manage.py shell (copy-paste) заполняем таблицу Publisher:
# from books.models import Publisher
# p1 = Publisher(name='Apress', address='2855 Telegraph Avenue',
# city='Berkeley', state_province='CA', country='U.S.A.',
# website='http://www.apress.com/')
# p1.save()
# p2 = Publisher(name="0'Reilly", address='10 Fawcett St.',
# city='Cambridge', state_province='MA', country='U.S.A.',
# website='http://www.oreilly.com/')
# p2.save()
# publisher_list = Publisher.objects.all()
# publisher_list

from vvkws.books.models import Book
def book_list(request):
    resrow = Book.objects.order_by('id')
    return render_to_response('book_list.htm',{'resrow':resrow})

# 9)
# Получаем информацию о браузере и параметрах системы клиента

# Вместо конструкции try:/except: используется метод .get()
def get_browser(request):
    ua = request.META.get('HTTP_USER_AGENT','unknown browser')
    return HttpResponse("Baш броузер : %s" % ua)

# Вывод словаря мета-данных
def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k,v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


# 10)
# Ввод данных в формы
def search_form(request):
    return render_to_response('search_form.htm')
# Вывод результата поиска
'''
def search(request):
    if 'q' in request.GET:
        message = 'Вы искали: %r' % request.GET['q']
    else:
        message = 'Вы отправили пустую форму.'
    return HttpResponse(message)
'''
# -''-''-''-''- вариант 2 :
'''
def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        books = Book.objects.filter(title__icontains=q)
        return render_to_response('search_results.htm',
            {'books':books,'query':q})
    else:
#       return HttpResponse('Введите поисковый запрос.')
        return render_to_response('search_form.htm',{'error':True})
'''
# -''-''-''-''- вариант 3,4 :
def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Введите поисковый запрос.')
        elif len(q) <4 or len(q)>10:
            errors.append('Введите от 4 до 10 символов.')
        else:
            books = Book.objects.filter(title__icontains=q)
            return render_to_response('search_results.htm',{'books':books,'query':q})
    return render_to_response('search_form.htm',{'errors':errors})

"""
# Для тестов при посылке POST можно закоментировать в settings.py следующую строку:
# 'django.middleware.csrf.CsrfViewMiddleware'
def contact(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Введите тему.')
        if not request.POST.get('message', ''):
            errors.append('Введите сообщение.')
        if request.POST.get('email') and '@' not in request.P0ST['email']:
            errors.append('Bведён неправильный адрес e-mail.')
        if not errors:
            send_mail(
                request.P0ST['subject'],
                request.P0ST['message'],
                request.POST.get('email', 'noreply@vvknb.khome.ua'),
                ['root@vvknb.khome.ua'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    return render_to_response('contact_form.htm',{
        'errors' : errors,
        'subject': request.POST.get('subject', ''),
        'message': request.POST.get('message', ''),
        'email'  : request.POST.get('email'  , ''),
    })
"""

# формы через django 
# по соглашению сообщества формы пишем в forms.py, в urls.py подключаем этот файл, так же, 
# как и views.py: from vvkws.forms import * , а в этом файле включаем нижеприведённой строкой:
from forms import ContactForm
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email','noreply@vvknb.khome.ua'),       # From:
                ['vvkpl@polly.com.ua' ],                        # To:
            )
            return HttpResponseRedirect('/contact/thanks')
    else:
        form = ContactForm(
            initial={'subject':'This is only teeessst...'}
        )
    return render_to_response('contact_form.htm',{'form':form})

# 11)
# Приёмы программирования на Django
# Список объектов (не разобранный пример):
def object_list(request,model):
    obj_list = model.objects.all()
    template_name = 'vvkws/%s_list.html' % model.name.lower()
    return render_to_response(template_name,{'object_list':obj_list})
# urls.py:
#   (r'^events/$', object_list, {'model': models.Event}),
#   (r'^blog/entries/$', object_list, {'model': models.BlogEntry}),
# нет описания models. 

# 12)
# Вывод данных в PDF
from reportlab.pdfgen import canvas
def hello_pdf(request):
    # Создать объект HttpResponse с заголовками для формата PDF.
    response = HttpResponse(mimetype='application/pdf')
    response['Contenet-Disposition'] = 'attachment; filename=hello.pdf'
    # Создать объект PDF, передав объект ответа в качестве "файла"
    p = canvas.Canvas(response)
    # Нарисовать нечто в PDF. Именно здесь происходит создание содержимого PDF-документа.
    # Полное описание функциональности см. в документации ReportLab.
    p.drawString(100, 100, "Hello world.")
    # Закрыть объект PDF, все готово.
    p.showPage(); p.save()
    return response

from cStringIO import StringIO
def string_pdf(request):
    # Создать объект HttpResponse с заголовками для формата PDF.
    response = HttpResponse(mimetype='application/pdf')
    response['Contenet-Disposition'] = 'attachment; filename=hello.pdf'
    temp = StringIO()
    # Создать объект PDF, используя объект StringIO в качестве "файла"
    p = canvas.Canvas(temp)
    # Нарисовать нечто в PDF. Именно здесь происходит создание содержимого PDF-документа.
    # Полное описание функциональности см. в документации ReportLab.
    p.drawString(50, 50, "Hello world, my friend!")
    # Закрыть объект PDF, все готово.
    p.showPage(); p.save()
    # Получить значение из StringIO и записать его в ответ
    response.write(temp.getvalue())
    return response

# 13)
# Аутентификация
from django.contrib import auth
def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Пароль правилен и пользователь "активный"
        auth.login(request, user)
        # Переадресовать на страницу успешного входа,
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # Переадресовать на страницу ошибок
        return HttpResponseRedirect("/account/invalid/")

def logout_view(request):
    auth.logout(request)
    # Переадресовать на страницу успешного выхода,
    return HttpResponseRedirect("/account/loggedout/")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
        return HttpResponseRedirect("/books/")
    else:
        form = UserCreationForm()
    return render_to_response("register.htm", {
        'form' : form ,
        })




