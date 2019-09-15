from collections import OrderedDict

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from cartapp.models import *
from goodspost.models import *
from utils.cartmanager import *
from utils.log import *

class Cartview(View):
    def get(self,request):
        user = get_user(request)
        cartdict = OrderedDict()

        if user:
            cartlist = Cartitem.objects.filter(user_id=user.id)
        else:
            # cartlist = request.session.get('cart', {}).values()
            cartlist = Sessionmanager(request).select_all()
            log(cartlist)

            log(type(cartlist))

        if cartlist:
            for i in cartlist:
                # if isinstance(i, str):
                    # i = jsonpickle.loads(i)
                    # log(i)
                i = i()
                    # log(i)
                if not i.isdelete:

                    cartdict[i] = {'goods': i.get_Goods(),
                                   'size': i.get_Gsize(),
                                   'color': i.get_Gcolor(),
                                   'count:': i.count,
                                   }
        else:
            cartdict = {}
        # print(cartdict)
        context={'cartdict': cartdict,}
        return render(request, 'prepay.html', context)

    def post(self,request):
        kwargs = request.POST.dict()
        print(kwargs)
        flag = request.POST.get('flag', '')
        if flag == 'add':
            cartobj = Cartmanager(request, **kwargs)
            cartobj.add()
            print('request: ', request.POST.dict())
            # print(cartobj)
            # print(type(cartobj))
        elif flag == 'plus':
            cartobj = Cartmanager(request, **kwargs)
            log(request.POST.dict())
            cartobj.update_(1)
            log(cartobj.count)
        elif flag == 'minus':
            cartobj = Cartmanager(request, **kwargs)
            cartobj.update_(-1)
        elif flag == 'delete':
            cartobj = Cartmanager(request, **kwargs)
            cartobj.delete_()

        return redirect('prepay')




