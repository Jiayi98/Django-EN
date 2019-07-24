# Generated by Django 2.2.1 on 2019-07-24 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20190724_1107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project2expert',
            options={'managed': True, 'ordering': ('-itv_stime',)},
        ),
        migrations.AlterField(
            model_name='project2expert',
            name='itv_duration',
            field=models.IntegerField(blank=True, default=0, verbose_name='访谈时长'),
        ),
    ]
