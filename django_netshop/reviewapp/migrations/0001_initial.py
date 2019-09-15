# Generated by Django 2.2 on 2019-05-09 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('out_trade_num', models.UUIDField()),
                ('order_num', models.CharField(max_length=50)),
                ('trade_no', models.CharField(default='', max_length=120)),
                ('status', models.CharField(default='待支付', max_length=20)),
                ('payway', models.CharField(default='alipay', max_length=20)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.Address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Orderitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodsid', models.PositiveSmallIntegerField()),
                ('sizeid', models.PositiveSmallIntegerField()),
                ('colorid', models.PositiveSmallIntegerField()),
                ('count', models.PositiveSmallIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewapp.Order')),
            ],
        ),
    ]
