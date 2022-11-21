#!/usr/bin/python
# coding=utf8; version=2013050222; title='Набор дополнительных функций Python от VVK'

import os, sys
import time, datetime
import re, logging, ConfigParser
import select, tty
import socket
import signal, psutil
from logging import *


################################################################################
# СИСТЕМА
################################################################################

#-------------------------------------------------------------------------------
# Для вывода в консоли и в логах устанавливаем кодировку по-умолчанию: charset('utf8')
def charset(code):
    reload(sys); sys.setdefaultencoding(code);
    return None
#-------------------------------------------------------------------------------
# Выполнение системной комманды на стандартный вывод: runs('ls -l')
def runs(args):
    os.system("".join(args));
    return None
#-------------------------------------------------------------------------------
# Выполнение системной комманды с выводом в переменную кол-ва выводимых строк и
# самих строк буфера вывода (соответственно 1я и 2я возвращаемая переменная).
def runp(args):
    pout=os.popen("".join(args)).readlines(); lout=len(pout);
    return(lout,"".join(pout))
#-------------------------------------------------------------------------------



################################################################################
# ЧАСЫ
################################################################################

#-------------------------------------------------------------------------------
# Набор из 10 основных и одного резервного таймера (фактически считается коло-во вызовов данной функции)
# При вызове функции, указываем номер таймера и максимальное значение счётчика
# Функция возвращает -1, если таймер с указанным номером сработал (достиг max значения)
# или какое-то текущее значение таймера, если таймер ещё в работе (max значение ещё не достигнуто)
cnt=[0,0,0,0,0,0,0,0,0,0,0]
def timer(num,max):
    # Если номер таймера вне диапазона - присваеваем ему резервное значение
    if(num not in range(0,10)): num=10
    # Проверяем диапазон значений таймера
    if(max > 0xffffffffffffffff ): max=0xffffffffffffffff
    # Обнуление таймера
    if(max== 0): cnt[num]=0; return(0);
    # Текущее значение таймера
    if(cnt[num]<max-1): cnt[num]+=1; return(cnt[num]);
    # Если таймер сработал (достиг максимального значения) вернуть -1
    return(-1);
#-------------------------------------------------------------------------------
# Такой же самый таймер, только считает кол-во миллисекунд от последнего вызова
gms=[0,0,0,0,0,0,0,0,0,0,0]
def gmsec(num,max):
    if(num not in range(0,10)): num=10
    if(max > 0xffffffffffffffff ): max=0xffffffffffffffff
    ctm=int(round(time.time()*1000))
    if(gms[num]==0): gms[num]=ctm
    if(max== 0): gms[num]=ctm; return(0);
    raz=ctm-gms[num]
    if(raz<max-1): return(raz);
    return(-1);
#-------------------------------------------------------------------------------
# Пример исользования и вызова функций таймеров (time.sleep(0.1) можно не писать)
# while(1):
#   time.sleep(0.1); sec=0;                                         # ждём 100 мс
#   if(vvk.gmsec(1,1000)<0): vvk.gmsec(1,0); sec=vvk.timer(1,5);    # каждую секунду
#   if(sec<0): vvk.timer(1,0); print "Прошло 5 секунд..."           # 
#-------------------------------------------------------------------------------



################################################################################
# ФАЙЛЫ
################################################################################

# ТЕКСТОВЫЕ
#-------------------------------------------------------------------------------
# Строковый буфер и количество строк считанного файла
rsbuf=[]; rlbuf=0;
wsbuf=[]; wlbuf=0; wf=None;
#-------------------------------------------------------------------------------
# Чтение текстового файла (файла конфигурации) в буфер
# read-читает сиволы(len-байты), readline-строку(len-байты), readlines-все строки(len-строки)
# Функция возвращает количество считанных строк, это же значение записывается в rlbuf
# Если при чтении произошла ошибка, rlbuf = 0
def fl_readt (file):
    global rsbuf, rlbuf
    if(os.access(file,os.R_OK)):
        try:
            f=open(file,'r'); rsbuf=f.readlines(); f.close(); rlbuf=len(rsbuf)
        except (ValueError,IOError): rlbuf=0
        return(rlbuf);
#-------------------------------------------------------------------------------
# Запись в текстовый файл буфера строк. 
# Перед записью, строки должны находится в буфере wsbuf
# Функция возвращает количество записанных строк, это же значение записывается в wlbuf
# Если при записи произошла ошибка, wlbuf = 0
def fl_writt (file,m=[0,0,0]):
    global wsbuf, wlbuf, wf
    wlbuf= len(wsbuf)
    try:
        if(m[0] and not wf): wf=open(file,'w+')
        if(m[1] and wf and wlbuf>0): wf.writelines(wsbuf)
        if(m[2] and wf): wf.close(); wf=None
    except (ValueError,IOError): wlbuf=0
    return(wlbuf);
#-------------------------------------------------------------------------------
# Пример использования функций чтения и записи текстовых файлов:
# if os.access(file,os.R_OK): fl_readt(file)   # файл считан в rsbuf
# wsbuf=rsbuf
# запись буфера строк wsbuf в файл: [1-открытие, 1-запись, 1-закрытие]
# r=fl_writt('py_test_01.txt',[1,1,1])
# r=fl_writt('py_test_02.txt',[1,0,0]); wsbuf.append("var_stroka_03=\"Дополнительная строка\"")
#   fl_writt('',[0,1,0]); fl_writt('',[0,0,1])
#-------------------------------------------------------------------------------


# ЛОГИ
#-------------------------------------------------------------------------------
# Определение имени лог-файла, режима записи данных по-умолчанию и формат записи лог-данных
# Режимы записи данных: LV = DEBUG, INFO, WARNING, ERROR, CRITICAL
def logi(LV=logging.DEBUG,FL=u'myprog.log'):
#   logging.basicConfig(format = u'[%(asctime)s] %(levelname)-8sin \'%(module)s\' at line %(lineno)d: %(message)s', level=LV, filename=FL)
    logging.basicConfig(format = u'[%(asctime)s] %(levelname)-8s%(message)s', level=LV, filename=FL)
#---------------------------
# Тоже самое, только формат записи данных попроще (Записываются ТОЛЬКО данные)
def logd(LV=logging.DEBUG,FL=u'myprog.dat'):
    logging.basicConfig(format = u'%(message)s', level=LV, filename=FL)
#---------------------------
# Запись сообщения в лог-файл LV-loglevel, MS-message
# LV = DEBUG, INFO, WARNING, ERROR, CRITICAL
# если файл определён с режимом DEBUG, в него пишется всё, если с режимом ERROR, то только ERROR и CRITICAL
def logw(LV,MS):
    logging.log(LV,MS)
#---------------------------
# Закрытие записи в лог-файл
def logr():
    loghand = logging.getLogger()
    if loghand.handlers:
        for handler in loghand.handlers: loghand.removeHandler(handler)
#-------------------------------------------------------------------------------
# Пример использования функций работы с лог-файлом
# logi(LV=DEBUG,FL='py_test_01.log')                            # определение файла вывода с режимом записи DEBUG
# logw(DEBUG,u"Значения: n=%d r=%d var1=%s" % (n,r,var1))       # запись в лог-файл
# logw(INFO ,"Вариант2: n=%d r=%d var2=\"%s\"" % (n,r,var2))    #
# logr()                                                        # закрытие текущего лог-файла
# logd(LV=DEBUG,FL='py_test_01.ddd')                            # открываем лог-файл с форматом записи ТОЛЬКО данных
# logw(DEBUG,"---------------------------------------------")   # в него запишится линия без указания даты, режима, ...
# logr()     # если лог-файл не определён (или не открыт), то вывод будет на консоль
#-------------------------------------------------------------------------------

# КОНФИГИ (INI)
#-------------------------------------------------------------------------------
cfg_desc=None; cfg_file=''
#-------------------------------------------------------------------------------
# Инициализация файла конфигурации (определение дескриптора файла)
def cfg_init(file): 
    global cfg_desc,cfg_file; cfg_desc=ConfigParser.RawConfigParser(); cfg_file=file;
# Добавление секции к буферу конфигурации
def cfg_adds(section):
    global cfg_desc,cfg_file; cfg_desc.add_section(section);
# Устанавливает в указанной секции переменную var в значение val
def cfg_setv(section, var, val): 
    global cfg_desc,cfg_file; cfg_desc.set(section, var, val);
# Запись буфера конфигурации в файл
def cfg_writ(): 
    global cfg_desc,cfg_file; f=open(cfg_file,'wb'); cfg_desc.write(f);
# Чтение файла конфигурации в буфер конфигурации
def cfg_read(file): 
    global cfg_desc,cfg_file; cfg_desc.read(file);
# Получение булеевской переменной
def cfg_getb(section,var):
    global cfg_desc,cfg_file; r=cfg_desc.getboolean(section,var); return(r);
# Получение целочисленной переменной
def cfg_geti(section,var):
    global cfg_desc,cfg_file; r=cfg_desc.getint(section,var); return(r);
# Получение переменной типа float
def cfg_getf(section,var):
    global cfg_desc,cfg_file; r=cfg_desc.getfloat(section,var); return(r);
# Получение строковой переменной
def cfg_gets(section,var):
    global cfg_desc,cfg_file;
    try: r=cfg_desc.get(section,var);
    except (ConfigParser.NoSectionError,ConfigParser.NoOptionError): r='';
    return(r);
#-------------------------------------------------------------------------------
# Пример вызова функций чтения и записи файла конфигурации
# vvk.cfg_read('config_1.ini')
# a_float = vvk.cfg_getf('Section1', 'a_float'); a_float = a_float + 15.11
# vvk.cfg_init('config_2.ini')
# vvk.cfg_adds('Section1')
# vvk.cfg_setv('Section1', 'a_float', '%f'%(a_float))
# vvk.cfg_writ()
#-------------------------------------------------------------------------------



################################################################################
# СТРОКИ
################################################################################

#-------------------------------------------------------------------------------
# Чтение переменной из файла или из ранее считанного буфера, если к указанному файлу нет доступа
#-----------------------------
# Переменная должна быть записана в следующем формате (без пробелов):
# variable="value"  или  variable='value' или variable  = value
# между знаком = и значением д.б. только один символ
#-----------------------------
# Пример вызова:
# n,r,enc=get_flval('.config','varname'); txt=enc.decode('base64','strict');
# if i<0 or r<0: print "Not find varname in config file."; sys.exit(1)
# print "i=",i,"  r=",r,"  txt=",txt; sys.exit(0)
#-----------------------------
# Возвращает:
# i = номер строки с переменной, r = позиция значения в строке, s = строковое значение переменной
#-----------------------------
def get_flvar(file,varname):
    global rsbuf, rlbuf
    f=os.access(file,os.R_OK)
    if f==True: b=fl_readt(file)
    else      : b=rlbuf
    if b<=0   : return(-1,-1,"")
    s=''; n=-1;
    for i in range(0,b):
        n,r=rsbuf[i].find(varname),-1
        if n>=0: r=rsbuf[i].find("=")
        if r> 0: s=rsbuf[i][r+2:-2]; break;
    if r<0: return(-1,-1,"")
    else  : return(i,r,s)
#-------------------------------------------------------------------------------
# Возвращает количество полей в строке, разделённых указанным разделителем
def how_fields(string,delim):
    lst= string.split(delim); hf=len(lst)
    return(hf)
#-------------------------------------------------------------------------------
# Получение из строки указанных по номеру полей. Поля указываются цифрами, кроме:
# L-последнее поле, * - все поля от последнего указанного номера до конца строки
# Возвращает строку из указанных полей
# Пример вызова: print get_fields("Hello my very nice green world !","0L 05* 015L")
# Вернёт: Hello ! Hello world ! Hello my world !
def get_fields(string,fields):
    sss=[]; lst=string.split(" "); l=len(lst); fld=(" ".join(fields)).split(" "); p=-1; n=0;
    for f in fld:
        if(f=='l' or f=='L'):   
            sss.append(lst[l-1]); p=l-1; continue;
        if(f!='*'):
            if(not f.isdigit()): continue;
            if(int(f)>=l): f=l-1
            sss.append(lst[int(f)]); p=int(f);
        else:
            for n in range(p+1,l): sss.append(lst[int(n)])
            p=n;
    return(" ".join (sss))
#-------------------------------------------------------------------------------
# Заменяем в строке string символы из массива D : D[x][0]-что меняем(s1), D[x][1]- на что меняем(s2)
# out=vvk.tr_chars( vvk.get_fields(a,'026L'), D=[('\[',''),('\]',''),('\,',''),('\'',''),] )
# Возвращает строку с изменёнными символами
def tr_chars(string,D):
    for d in range(0,len(D)):
        s1="\\%c"%D[d][0]
        s2=D[d][1]
        string=re.sub(s1,s2,string)
    return(string)
#-------------------------------------------------------------------------------
# Замена символа в строке по номеру символа
def ch_replace(string,index,newchar):
    s=list(string); l=len(s);
    if index >= l : index=l-1
    if str(newchar).isdigit(): char=chr(newchar);
    else                     : char=newchar;
    s[index] = char; string=''.join(s)
    return(string)
#-------------------------------------------------------------------------------



################################################################################
# СЕТЬ
################################################################################

#-------------------------------------------------------------------------------
# Получение IP-адреса по имени хоста
def get_ipaddress(hostname):
    try: 
        return socket.gethostbyname(hostname)
    except (socket.gaierror,socket.timeout):
        return None
#-------------------------------------------------------------------------------
# Получение имени хоста по IP-адресу
def get_hostname(ipaddr):
    try: 
        return socket.gethostbyaddr(ipaddr)[0]
    except socket.herror:
        return None
#-------------------------------------------------------------------------------



################################################################################
# ПРОЦЕССЫ
################################################################################

#-------------------------------------------------------------------------------
# Получение списка процессов
# При вызове в параметре указывается: P-pid процесса(частично), N-название(частично),
# U-пользователь, D-дата запуска(частично), S-статус(частично), T-терминал(частично).
# частично - это значит, что можно указывать часть строки, указанная подстрока ищется по всей строке 
# Например: ps=ps_list(P="23",N="py",U="root",D="201301232121",S="sleep",T="None")
# или вывод всех процессов с заданным именем: for a in ps_list(N='python'): print a
def ps_list(P=None,N=None,U=None,D=None,S=None,T=None,C=None):
    Z=0;
    if(P): Z+=1         # PID
    if(N): Z+=10        # NAME
    if(U): Z+=100       # USER
    if(D): Z+=1000      # DATE
    if(S): Z+=10000     # STAT
    if(T): Z+=100000    # TERM
    if(C): Z+=1000000   # CMDL
    r=[];
#   dtnow=str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    dtn=round(time.time());
    for a in range(0,4):
        ps=psutil.get_process_list();
        if(ps): break
        sleep(0.5)
    if(a>=3): return None
    for p in ps:
        if(not p): continue
        add=0
        d=str(datetime.datetime.fromtimestamp(p.create_time).strftime("%Y%m%d%H%M%S"))
        dtc=round(p.create_time)
        status=0
        terminal=0
        if(P and str(p.pid).find(P)     >-1): add+=1
        if(N and p.name.find(N)         >-1): add+=10
        if(U and p.username == U           ): add+=100
        if(D and d.find(D)              >-1): add+=1000
#       if(S and str(p.status).find(S)  >-1): add+=10000
#       if(T and str(p.terminal).find(T)>-1): add+=100000
        if(C and str(p.cmdline).find(C) >-1): add+=1000000
        if(P=="*" or N=="*" or U=="*" or D=="*" or S=="*" or T=="*" or C=="*"): add=Z=0
        if(add==Z):
            # Выводим процессы которые были запущены за 1,2 сек до этого (текущий процесс не выводим)
            if(dtn-dtc>2):
               #          P  N  U  D  S  T  C  :    P      N       U         D    S         T           C
               r.append("%d %s %s %s %s %s %s" % (p.pid, p.name, p.username, d,   status,   terminal, p.cmdline))
#              print p,"<------>",dtc,">",dtn
    return(r)
#-------------------------------------------------------------------------------
# Удаление процессов по указанным в параметре номерам процессов (PID)
# Возвращает 0, если ошибок не было или номер системной ошибки.
def ps_kill(PS=None):
    if not PS: return(0)
    pp="%s " % (PS.strip()); pp=pp.split(" "); ret=0;
    for p in pp: 
        if p:
            try: os.kill(int(p),signal.SIGKILL);
            except (os.error): ret=1;
    return(ret)
#-------------------------------------------------------------------------------



################################################################################
# КЛАВИАТУРА
################################################################################

#-------------------------------------------------------------------------------
kb_poll=None; kb_attr=None; kb=[0,0,0,0,0,0,0]
#-------------------------------------------------------------------------------
# Инициализация чтения нажатий клавиш (через дескриптор файла stdin)
def kb_init():
    global kb_poll, kb_attr
    kb_attr = tty.tcgetattr(sys.stdin)
    kb_poll = select.poll()
    kb_poll.register(sys.stdin,select.POLLIN)
    tty.setcbreak(sys.stdin)
def kb_exit():
    global kb_poll, kb_attr
    sys.stdin.flush()
    tty.tcsetattr(sys.stdin,tty.TCSADRAIN,kb_attr)

#--------------------------------------------
# Чтение последней нажатой клавиши...
def kb_last():
    global kb_poll, kb
    kb=[0,0,0,0,0,0,0]; f=0;
    if(not kb_poll): kb_init()
    if(not kb_poll): return(kb)
    events = kb_poll.poll(100)
    if  events:
        # Читать код нажатой клавиши
        kb[0]=ord(sys.stdin.read(1))
        # Если считан расширенный код
        if (kb[0] == 27):
            # ESC - считывается при двойном нажатии
            kb[1] = ord(sys.stdin.read(1))
            # F1-F4, Alt+key
            if((kb[1]!= 27  and kb[1]!= 0) and (kb[1]<92 and (kb[1]<36 or kb[1]>59))):
                kb[2] = ord(sys.stdin.read(1))
            # PgUp,PgDn, Alt+F
            if((kb[1]== 91  or kb[1]== 79) and (kb[2]  < 65)):
                kb[3] = ord(sys.stdin.read(1))
            # F5-F8, f=1 - Ctrl,Alt+стрелки
            if (kb[1]== 91  and kb[2]==49  and  kb[3] != 126):
                kb[4] = ord(sys.stdin.read(1)); f=1;
            # F9-F12, Alt+F
            if((kb[1]== 91  and kb[2]==50  and  kb[3] != 126) or (kb[1]==79 and kb[3]==59) or 
               (kb[1]== 91  and kb[3]==59  and  f==0)):
                kb[4] = ord(sys.stdin.read(1))
            # Ctrl, Alt, Shift + Fx
            if (kb[1]== 91  and kb[4]==59  and  kb[3] != 126):
                kb[5] = ord(sys.stdin.read(1))
                kb[6] = ord(sys.stdin.read(1))
            # Alt+F1-F4, Alt+PgUP(PgDn)
            if((kb[1]== 79  and kb[3]==59)  or (kb[1]==91 and kb[3]==59)):
                kb[5] = ord(sys.stdin.read(1))
    return(kb)
#-------------------------------------------------------------------------------
# Пример программы обработки нажатий клавиш:
# def mexit():
#     sys.stdin.flush(); kb_exit(); print "Выход..."; sys.exit(0)
# def pubcycle():
#     try:
#         while True:
#             kb_last()
#             if(kb[0] >  0): print kb
#             if(kb[0]==113): break # выход по клавише q
#             time.sleep(0.1)
#     except (KeyboardInterrupt): print "CTRL+C"; mexit()
# print "Вывод кодов нажатых клавиш. Выход - q:"; pubcycle(); mexit()
#-------------------------------------------------------------------------------

