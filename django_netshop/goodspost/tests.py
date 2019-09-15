import time

from django.db.transaction import atomic
from django.test import TestCase
from goodspost.models import *
import json

# Create your tests here.


@atomic
def installdata():
    import json
    with open('data.json', 'r') as f:
        li = json.loads(f.read())
    for cat in li:
        if Category.objects.filter(cname=cat.get('category')):
            cate = Category.objects.get(cname=cat.get('category'))
        else:
            cate = Category.objects.create(cname=cat.get('category'))
        for gds in cat.get('goods'):
            if gds != []:
                if Goods.objects.filter(gname=gds.get('goodsname'), cate=cate, gdesc=gds.get('goods_desc')
                                             , price=gds.get('goods_price'), oldprice=gds.get('goods_oldprice')):

                        goods = Goods.objects.get(gname=gds.get('goodsname'), cate=cate, gdesc=gds.get('goods_desc')
                                                , price=gds.get('goods_price'), oldprice=gds.get('goods_oldprice'))
                else:
                    goods = Goods.objects.create(gname=gds.get('goodsname'), cate=cate, gdesc=gds.get('goods_desc')
                                             , price=gds.get('goods_price'), oldprice=gds.get('goods_oldprice'))
            sizeslist = []
            for sizes in gds.get('sizes'):
                if Gsize.objects.filter(sname=sizes[0]):
                    size = Gsize.objects.get(sname=sizes[0])
                else:
                    size = Gsize.objects.create(sname=sizes[0])
                sizeslist.append(size)

            colorlist = []
            for colors in gds.get('colors'):
                if Gcolor.objects.filter(colorname=colors[0], colorurl=colors[1]):
                    color = Gcolor.objects.get(colorname=colors[0], colorurl=colors[1])
                else:
                    color = Gcolor.objects.create(colorname=colors[0], colorurl=colors[1])
                colorlist.append(color)
            for size in sizeslist:
                for color in colorlist:
                    if Inventory.objects.filter(color=color, size=size, goods=goods):
                        pass
                    else:
                        Inventory.objects.create(color=color, size=size, goods=goods)
            for gdetail in gds.get('specs'):
                gdetailname = Goodsdname.objects.create(gdname=gdetail[0])
                for gdurl in gdetail[1]:
                    if Goodsdetail.objects.filter(gdetailname=gdetailname, gdurl=gdurl, goods=goods):
                        pass
                    else:
                        Goodsdetail.objects.create(gdetailname=gdetailname, gdurl=gdurl, goods=goods)

