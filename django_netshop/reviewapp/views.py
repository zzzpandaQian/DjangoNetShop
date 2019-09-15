import uuid

import jsonpickle
from django.db.models import F
from django.db.transaction import atomic
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from reviewapp.models import Order, Orderitem
from userapp.models import Address
from utils.alipay import *
# Create your views here.
from django.views import View
import datetime
from cartapp.models import Cartitem
from goodspost.models import Goods, Inventory
from utils.log import log

class Orderview(View):
    def get(self, request):
        factorlist = request.GET.get('factorlist', '')
        print(factorlist)
        redirect_para = request.GET.get('redirect', '')
        user = request.session.get('user', '')
        if not user:
            url = '/user/login/?redirect={}&factorlist={}'.format(redirect_para, factorlist)
            return HttpResponseRedirect(url)
        return HttpResponseRedirect('/orderlogin/?factorlist=%s' % factorlist)


def orderlogin(request):
    user = request.session.get('user', '')
    if user:
        user = jsonpickle.loads(user)

    factorlist = request.GET.get('factorlist')
    if factorlist:
        factorlist = jsonpickle.loads(factorlist)
        cartlist = (Cartitem.objects.get(**i, user=user, isdelete=False) for i in factorlist)
    else:
        cartlist = []
    addr = user.address_set.get(isdefault=True)

    return render(request, 'order.html', {'addr': addr, 'cartlist': cartlist})


alipayobj = AliPay(appid='2016093000633836', app_notify_url='http://127.0.0.1:8000/order/checkpay/',
                   app_private_key_path='reviewapp/keys/my_private_key.txt',
                   alipay_public_key_path='reviewapp/keys/alipay_public_key.txt',
                   return_url='http://127.0.0.1:8000/order/checkpay/', debug=True)


@atomic
def toorder(request):
    addrid = int(request.GET.get('address', -1))
    addr = Address.objects.get(id=addrid)

    payway = request.GET.get('payway', '')
    log('payway:', payway)
    cartitem = request.GET.get('cartitems', '')
    user = request.session.get('user', '')
    if not user:
        return redirect('orederhome')
    user = jsonpickle.loads(user)
    log('user:', user)
    if cartitem:
        cartitem = jsonpickle.loads(cartitem)
    log('cartitem', cartitem)
    order = Order.objects.create(
        out_trade_num=uuid.uuid4().hex,
        order_num=datetime.datetime.today().strftime('%y%m%d%H%M%S'),
        payway=payway,
        address=addr,
        user=user

    )

    total = int(request.GET.get('tp', 0))
    log('total ', total)
    log('total获取成功')
    orderitems = [Orderitem.objects.create(order=order, **i) for i in cartitem]
    # log('orderitems: ', orderitems)
    log('Orderitem创建成功')
    alipayParams = alipayobj.direct_pay(subject='天猫超市', out_trade_no=order.out_trade_num, total_amount=total)
    url = alipayobj.gateway + '?' + alipayParams
    log('url: ', url)
    log('url地址生成成功')
    return HttpResponseRedirect(url)


def checkpay(request):
    # 获取参数
    params = request.GET.dict()
    log('params :', params)
    # 获取签名
    sign = params.pop('sign')
    user = jsonpickle.loads(request.session.get('user'))
    trade_num = params.get('trade_no', '')
    out_trade_no = params.get('out_trade_no', '')
    order = Order.objects.get(out_trade_num=out_trade_no)
    order.status = '待发货'
    order.trade_no = trade_num
    order.save()
    orderlist = order.orderitem_set.all()
    invupdate = [Inventory.objects.filter(goods=i.goodsid, color=i.colorid, size=i.sizeid).update(count=F('count') - int(i.count)) for i in orderlist]
    cartitemupdate = [Cartitem.objects.filter(goodsid=i.goodsid, colorid=i.colorid, sizeid=i.sizeid, count=i.count, user=user).update(isdelete=True) for i in orderlist]

    # 判断是否支付成功
    flag = alipayobj.verify(params, sign)
    if flag:
        return HttpResponse('支付成功')
    return HttpResponse('支付失败')
