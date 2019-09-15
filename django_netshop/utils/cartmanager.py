from collections import OrderedDict

import jsonpickle
from django.db.models import Manager, F

from cartapp.models import Cartitem
from utils.log import log


class defManager(object):
    def add(self, goodsid, colorid, sizeid, count, *args, **kwargs):
        '''添加商品，如果商品已经存在就更新商品的数量(self.update_())，否则直接放到购物车'''
        pass

    def delete_(self, goodsid, colorid, sizeid, *args, **kwargs):
        '''删除一个购物项'''
        pass

    def update_(self, goodsid, colorid, sizeid, count, step, *args, **kwargs):
        '''更新购物项的数据,添加减少购物项数据'''
        pass

    def select_all(self, *args, **kwargs):
        ''':return CartItem  多个购物项'''
        pass


class Usermanager:
    def __init__(self, user, goodsid, colorid, sizeid, count, *args, **kwargs):
        self.user = user
        self.args_1 = dict(goodsid=goodsid, colorid=colorid, sizeid=sizeid, user=self.user, isdelete=False)
        self.count = count

    def add(self):
        # 判断是否存在
        if not Cartitem.objects.filter(**self.args_1):
            Cartitem.objects.create(count=self.count, **self.args_1)

    def delete_(self):
        # 逻辑删除
        Cartitem.objects.filter(**self.args_1).update(isdelete=True, count=0)

    def select_all(self):
        return Cartitem.objects.filter(user=self.user)

    def update_(self, step):
        Cartitem.objects.filter(**self.args_1).update(count=F('count') + int(step))


class Sessionmanager:
    def __init__(self, request, *args, **kwargs):
        # 获得各参数字典args_2, session['cart']为存放无主键的Cartitem对象的有序字典
        # 将'goodsid, sizeid, colorid'作为session['cart']的key值
        self.session = request.session
        self.args_2 = dict(goodsid=kwargs.get('goodsid', 0), colorid=kwargs.get('colorid', 0),
                           count=kwargs.get('count', 0), sizeid=kwargs.get('sizeid', 0), isdelete=False)

        self.count = int(kwargs.get('count', 0))

        if 'cart' not in request.session:
            request.session['cart'] = OrderedDict()
        self.cart = self.session['cart']

        self.key = str(kwargs.get('goodsid', 0)) + ',' + str(kwargs.get('colorid', 0)) + ',' + str(
            kwargs.get('sizeid', 0))

    def add(self):
        # 判断是否已经存在key
        # 否则新增item
        key = self.key
        if key in self.cart:
            jsonpickle.loads(self.cart[key]).count = self.count

        self.cart[key] = jsonpickle.dumps(Cartitem(**self.args_2))
        self.session.save()

    def select_all(self):
        queryset = self.cart.values()
        if queryset:
            return [jsonpickle.loads(i) for i in queryset]
        else:
            return []

    def delete_(self):
        key = self.key
        if key in self.cart:
            del self.cart[key]

        self.session.save()

    def update_(self, step):
        Cartitem.objects.filter(**self.args_2).update(count=F('count') + int(step))

    def migrateSession2DB(self):
        # 对session['cart']中的values进行数据库牵引
        # 即在数据库保存Cartitem对象， 并删除session['cart']的数据
        user = self.session.get('user', '')
        print('user:', user)
        if user:
            user_ = jsonpickle.loads(user)
            for cartitem in self.select_all():
                if Cartitem.objects.filter(goodsid=cartitem.goodsid, colorid=cartitem.colorid,
                                           sizeid=cartitem.sizeid).count() == 0:
                    cartitem.user = user_
                    cartitem.save()
                    print('新增物品')
                else:
                    item = Cartitem.objects.get(goodsid=cartitem.goodsid, colorid=cartitem.colorid,
                                                sizeid=cartitem.sizeid)
                    item.count = int(item.count) + int(cartitem.count)
                    item.save()
                    print('扩增物品')

        del self.cart
        self.session.save()
        print('删除完成')


def Cartmanager(request, *args, **kwargs):
    # 针对post响应返回不同类型manager
    user = request.session.get('user', '')
    if user:
        user = jsonpickle.loads(user)
        return Usermanager(user, *args, **kwargs)
    return Sessionmanager(request, *args, **kwargs)
