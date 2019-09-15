# from userapp.models import *
# from cartapp.models import *
# user = Account.objects.get(id=1)
# from utils.cartmanager import *
# cart = Usermanager(user, goodsid=4, sizeid=4, colorid=1, count=2, csrf='1111')
# cart.args_1
# cart.update(1)
# cart.delete()

a1 = {'a':1, 'b':2}



class dic:
    def __init__(self,*args, **kwargs):
        self.b = dict(a=kwargs.get('a','2'))

    def ha(self):
        print(self.b, 111)

dic(**a1).ha()