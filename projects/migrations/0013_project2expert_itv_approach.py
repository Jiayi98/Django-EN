# Generated by Django 2.2.1 on 2019-08-07 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20190807_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='project2expert',
            name='itv_approach',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='咨询方式'),
        ),
    ]