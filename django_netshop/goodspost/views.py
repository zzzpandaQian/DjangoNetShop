import collections
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.views import View
from goodspost.models import *


class homeview(View):
    def get(self,request, num=2):
        # cate = Category.objects.get(id=num)
        index = request.GET.get('index', 1)
        print(index)
        category = Category.objects.all().order_by('id')
        gds = Goods.objects.filter(cate_id=num).order_by('id')
        page = Paginator(gds, 5)
        goods = page.page(index)
        print(request)


        return render(request, 'home.html', {'goods': goods, 'category': category, 'cid':int(num), 'num': index})

# HttpRequest


def recommend(func):
    # 添加猜你喜欢栏目元素（即浏览历史）
    def _wrapper(obj, request, num, *args, **kwargs):
        cate_id = request.GET.get('cate')
        good = str(num)
        # 根据类别的id来作为键，以防男装出现推荐女装商品的情况
        reclist = request.COOKIES.setdefault(cate_id,'')
        reclist = reclist.strip().split()
        # 获取goods列表
        pre_reclist = [Goods.objects.get(id=int(i)) for i in reclist]
        response = func(obj, request, num, pre_reclist, *args, **kwargs)

        # 去重
        if good in reclist:
            reclist.remove(good)
            reclist.insert(0, good)

        # 将列表长度控制在4
        elif len(reclist) < 4:
            reclist.append(good)
        # 确保最近浏览的在首位
        else:
            reclist.pop()
            reclist.insert(0, good)
        response.set_cookie(str(cate_id), ' '.join(reclist), max_age=3*24*60*60)

        return response

    return _wrapper


class detailview(View):
    @recommend
    def get(self,request, num, pre_reclist=[]):
        num = int(num)
        gd = Goods.objects.get(id=num)
        # 获取相关colors和sizes列表
        colors = gd.get_color_size('color', Gcolor)
        sizes = gd.get_color_size('size', Gsize)
        # 获取首个库存元素
        inv = gd.inventory_set.first()
        # 获取商品详情栏的具体内容(包括整体款式模特实拍参数规格等)
        # 通过有序字典的形式存储
        gddict = gd.get_gddict()
        # 生成猜你喜欢(浏览记录)列表
        pre_reclist = pre_reclist

        context = {
            'gd': gd,
            'colors': colors,
            'sizes': sizes,
            'inv': inv,
            'gddict': gddict,
            'reclist': pre_reclist,
        }
        return render(request, 'detail.html', context)
