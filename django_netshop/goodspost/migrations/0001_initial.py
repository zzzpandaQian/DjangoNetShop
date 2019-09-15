# Generated by Django 2.2 on 2019-04-27 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 't_cate',
            },
        ),
        migrations.CreateModel(
            name='Gcolor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colorname', models.CharField(max_length=10)),
                ('colorurl', models.ImageField(upload_to='color/')),
            ],
            options={
                'db_table': 't_gcolor',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gname', models.CharField(max_length=20, unique=True)),
                ('gdesc', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('oldprice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goodspost.Category')),
            ],
            options={
                'db_table': 't_goods',
            },
        ),
        migrations.CreateModel(
            name='Goodsdname',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gdname', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 't_gdname',
            },
        ),
        migrations.CreateModel(
            name='Gsize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sname', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 't_gsize',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=100)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goodspost.Gcolor')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goodspost.Goods')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goodspost.Gsize')),
            ],
            options={
                'db_table': 't_inventory',
            },
        ),
        migrations.CreateModel(
            name='Goodsdetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gdurl', models.ImageField(upload_to='')),
                ('gdetailname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goodspost.Goodsdname')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goodspost.Goods')),
            ],
            options={
                'db_table': 't_gdetail',
            },
        ),
    ]
