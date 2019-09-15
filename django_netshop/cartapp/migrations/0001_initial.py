# Generated by Django 2.2 on 2019-05-07 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cartitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodsid', models.PositiveIntegerField()),
                ('colorid', models.PositiveIntegerField()),
                ('sizeid', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField()),
                ('isdelete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.Account')),
            ],
        ),
    ]