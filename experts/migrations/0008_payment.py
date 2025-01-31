# Generated by Django 2.2.1 on 2019-07-12 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experts', '0007_expertinfo_efee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('ep_id', models.AutoField(primary_key=True, serialize=False)),
                ('alipay', models.CharField(blank=True, max_length=150, null=True, verbose_name='支付宝')),
                ('bank', models.CharField(blank=True, max_length=150, null=True, verbose_name='银行账号')),
                ('wechat', models.CharField(blank=True, max_length=150, null=True, verbose_name='微信支付')),
                ('remark', models.TextField(blank=True, max_length=150, null=True, verbose_name='备注')),
                ('eid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experts.ExpertInfo')),
            ],
            options={
                'db_table': 'payment',
                'managed': True,
            },
        ),
    ]
