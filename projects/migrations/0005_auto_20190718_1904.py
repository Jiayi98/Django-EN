# Generated by Django 2.2.1 on 2019-07-18 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20190718_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='pdetail',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='person_in_charge',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='我方项目对接人'),
        ),
        migrations.AddField(
            model_name='project',
            name='pm_wechat',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]