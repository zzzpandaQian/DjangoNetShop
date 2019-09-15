# Generated by Django 2.2 on 2019-05-06 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('areaid', models.IntegerField(primary_key=True, serialize=False)),
                ('areaname', models.CharField(max_length=50)),
                ('parentid', models.IntegerField()),
                ('arealevel', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
            options={
                'db_table': 'area',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.EmailField(max_length=254)),
                ('pwd', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 't_account',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aname', models.CharField(max_length=30)),
                ('phonenum', models.CharField(max_length=11)),
                ('addr', models.CharField(max_length=100)),
                ('isdefault', models.PositiveSmallIntegerField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.Account')),
            ],
            options={
                'db_table': 't_address',
                'managed': True,
            },
        ),
    ]
