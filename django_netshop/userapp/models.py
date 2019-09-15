from django.db import models

# Create your models here.
class Area(models.Model):
    areaid = models.IntegerField(primary_key=True)
    areaname = models.CharField(max_length=50)
    parentid = models.IntegerField()
    arealevel = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'area'
        unique_together = (('areaid', 'parentid'),)


class Account(models.Model):
    uname = models.EmailField()
    pwd = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 't_account'

    def __str__(self):
        return '%s'%(self.uname,)


class Address(models.Model):
    aname = models.CharField(max_length=30)
    phonenum = models.CharField(max_length=11)
    addr = models.CharField(max_length=100)
    isdefault = models.PositiveSmallIntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 't_address'

    def __str__(self):
        return '%s%d'%(self.aname, self.account_id)


