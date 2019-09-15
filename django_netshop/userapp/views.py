import hashlib

import jsonpickle
from django.core.serializers import serialize
from django.db.transaction import atomic
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from userapp.models import *
from utils.cartmanager import Sessionmanager
from utils.code import gene_code
from utils.log import log


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    @atomic
    def post(self, request):
        uname = request.POST.get('account', '')
        pwd = request.POST.get('password', '')
        log(pwd)
        if Account.objects.filter(uname=uname):
            return redirect('/user/register/')
        else:
            pwd = hashlib.sha256(pwd.encode('utf-8'))
            pwd1 = pwd.hexdigest()
            log(pwd1)
            user = Account.objects.create(uname=uname, pwd=pwd1)
            request.session['user'] = jsonpickle.dumps(user)
            # return redirect('/home/')
            return redirect('center')



def judge(request):
    uname = request.GET.get('uname')
    if Account.objects.filter(uname=uname):
        return JsonResponse({'flag': False})
    else:
        return JsonResponse({'flag': True})


class Center(View):
    def get(self, request):
        if request.session.get('user', '') == '':
            return redirect('login')
        else:
            return render(
                request,
                'center.html',
            )


class Login(View):
    def get(self, request):
        # request.session.flush()
        red = request.GET.get('redirect', '')
        factorlist = request.GET.get('factorlist', '')
        if red == 'red':
            return render(request, 'login.html', {'result': '', 'red': red})
        elif red == 'order':
            return render(request, 'login.html', {'result': '', 'red': red, 'factorlist': factorlist})
        return render(request, 'login.html', {'result': ''})


    def post(self, request):
        uname = request.POST.get('account')
        pwd = request.POST.get('password')
        pwd = hashlib.sha256(pwd.encode('utf-8'))
        pwd = pwd.hexdigest()
        user = Account.objects.get(uname=uname, pwd=pwd)
        factorlist = request.POST.get('factorlist', '')

        if user:
            request.session['user'] = jsonpickle.dumps(user)
            Sessionmanager(request).migrateSession2DB()

            if request.POST.get('redirect') == 'cart':
                return redirect('prepay')
            elif request.POST.get('redirect') == 'order':
                return HttpResponseRedirect('/orderlogin/?factorlist='+factorlist)
            return HttpResponseRedirect('/user/center/')
        else:
            return render(request, 'login.html', {'result': '用户或密码错误'})



class Loadcode(View):
    def get(self, request):
        img, txt = gene_code()
        request.session['sessioncode'] = jsonpickle.dumps(txt)
        return HttpResponse(img, content_type='img/png')


def checkcode(request):
    gtxt = request.GET.get('code')
    print('gtxt', gtxt)
    txt = request.session.get('sessioncode', '')
    if txt:
        txt = jsonpickle.loads(txt)
    print('txt', txt)
    if gtxt == txt:
        return JsonResponse({'checkFlag': True})
    return JsonResponse({'checkFlag': False})


def logout(request):
    request.session.clear()
    return JsonResponse({'flag': True})


class Address_view(View):
    def get(self,request):
        user_obj = jsonpickle.loads(request.session.get('user'))
        log(user_obj)
        print('user_obj:', user_obj.id)
        addrlist = Address.objects.filter(account_id=user_obj.id)
        print(addrlist)
        return render(request, 'adress.html', {'addrlist': addrlist})

    def post(self,request):
        aname = request.POST.get('user-name')
        phone = request.POST.get('user-phone')
        address = request.POST.get('detailarea')
        user_obj = jsonpickle.loads(request.session.get('user'))

        if Address.objects.filter(account_id=user_obj.id):
            isdel = 0
        else:
            isdel = 1
        account = jsonpickle.loads(request.session.get('user'))
        Address.objects.create(aname=aname, phonenum=phone, addr=address, account=account, isdefault=isdel)
        return redirect('addr')


def change_area(request):
    pid = int(request.GET.get('parentid', '-1'))
    arealist = Area.objects.filter(parentid=pid)
    arealist = serialize('json', arealist)
    return JsonResponse({'arealist': arealist})
