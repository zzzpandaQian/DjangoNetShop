from django.db import models

# Create your models here.
from goodspost.models import Gcolor, Goods, Gsize
from userapp.models import Account


class Cartitem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    isdelete = models.BooleanField(default=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = 't_cartitem'

    def __str__(self):
        return 'goods:%s,color:%s,size:%s,count:%s' % (self.goodsid, self.colorid, self.sizeid, self.count)

    def __call__(self, *args, **kwargs):
        return Cartnoid(self.goodsid, self.colorid, self.sizeid, self.count, self.isdelete)

    def get_Gcolor(self):
        return Gcolor.objects.get(id=self.colorid)

    def get_Gsize(self):
        return Gsize.objects.get(id=self.sizeid)

    def get_Goods(self):
        return Goods.objects.get(id=self.goodsid)


class Cartnoid:
    def __init__(self, g, c, s, co, isdel):
        self.goodsid = g
        self.colorid = c
        self.sizeid = s
        self.count = co
        self.isdelete = isdel

    def __str__(self):
        return 'goods:%s,color:%s,size:%s,count:%s' % (self.goodsid, self.colorid, self.sizeid, self.count)

    def get_Gcolor(self):
        return Gcolor.objects.get(id=self.colorid)

    def get_Gsize(self):
        return Gsize.objects.get(id=self.sizeid)

    def get_Goods(self):
        return Goods.objects.get(id=self.goodsid)
