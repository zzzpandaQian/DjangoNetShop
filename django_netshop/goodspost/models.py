import collections

from django.db import models


# Create your models here.



class Category(models.Model):
    cname = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return '%s'%self.cname

    class Meta:
        db_table = 't_cate'

class Goods(models.Model):
    gname = models.CharField(max_length=20, unique=True)
    gdesc = models.CharField(max_length=100)
    cate = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    oldprice = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '%s'%self.gname

    class Meta:
        db_table = 't_goods'

    def colorfirst(self):
        return self.inventory_set.first().color.colorurl

    def get_color_size(self, target, cls): # targt='color'/'size', cls=Gcolor/Gsize
        # 获取所有库存类型
        inv = self.inventory_set.all()
        # 库存类型针对target的id进行不重复分组
        traget_select = inv.values('%s__id'%target).distinct()
        # 获得target类元祖
        result = (cls.objects.get(id=int(i.get('%s__id'%target))) for i in traget_select)
        return result

    def get_gddict(self):
        gddict = collections.OrderedDict()
        gdetail = self.goodsdetail_set.all().values('gdetailname').distinct()
        for i in gdetail:
            # 获取键值（key）
            gdname = Goodsdname.objects.get(id=i.get('gdetailname')).gdname
            # 获取值（value）可为列表
            gdurl_ = Goodsdetail.objects.filter(gdetailname_id=i.get('gdetailname'))
            gddict[gdname] = gdurl_
        return gddict

class Goodsdname(models.Model):
    gdname = models.CharField(max_length=30)
    def __str__(self):
        return '%s'%self.gdname

    class Meta:
        db_table = 't_gdname'

class Goodsdetail(models.Model):
    gdurl = models.ImageField(upload_to='')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    gdetailname = models.ForeignKey(Goodsdname, on_delete=models.CASCADE)

    def __str__(self):
        return '%s%s'%(self.gdetailname, self.gdurl)
    class Meta:
        db_table = 't_gdetail'



class Gsize(models.Model):
    sname = models.CharField(max_length=10)
    def __str__(self):
        return '%s'%self.sname

    class Meta:
        db_table = 't_gsize'

class Gcolor(models.Model):
    colorname = models.CharField(max_length=10)
    colorurl = models.ImageField(upload_to='color/')


    class Meta:
        db_table = 't_gcolor'

    def __str__(self):
        return '%s'%self.colorname

class Inventory(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=100)
    size = models.ForeignKey(Gsize, on_delete=models.CASCADE)
    color = models.ForeignKey(Gcolor, on_delete=models.CASCADE)
    def __str__(self):
        return '%d'%(id)

    class Meta:
        db_table = 't_inventory'


