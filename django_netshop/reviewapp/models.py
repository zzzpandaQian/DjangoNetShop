from django.db import models

# Create your models here.
from userapp.models import Address, Account


class Order(models.Model):
    out_trade_num = models.UUIDField()
    order_num = models.CharField(max_length=50)
    trade_no = models.CharField(max_length=120, default='')
    status = models.CharField(max_length=20, default='待支付')
    payway = models.CharField(max_length=20, default='alipay')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return '%s%s'%(self.out_trade_num, self.order_num)

    class Meta:
        db_table = 't_order'

class Orderitem(models.Model):
    goodsid = models.PositiveSmallIntegerField()
    sizeid = models.PositiveSmallIntegerField()
    colorid = models.PositiveSmallIntegerField()
    count = models.PositiveSmallIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return 'goodsid:%d, sizeid:%d, colorid:%d, count:%d'%(self.goodsid, self.sizeid, self.colorid, self.count)


    class Meta:
        db_table = 't_orderitem'