from django.db import models
from django.urls import reverse

# Create your models here.
class Client(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=150, blank=True, null=True, verbose_name='客户名称')
    bc_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='主业务联系人')
    fc_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='主财务联系人')
    half_hrs = models.IntegerField(choices=[(1, '可半小时'), (0, '不可半小时'), (2,'未知')], default=2, verbose_name='是否支持半小时访谈')
    ctype = models.CharField(max_length=50,blank=True,null=True,verbose_name='客户类型')
    cinfo = models.TextField(blank=True, null=True,verbose_name='客户介绍')
    class Meta:
        managed = True
        db_table = 'client_info'

    def __str__(self):
        return "{}-{}".format(self.cid, self.cname)

    def get_absolute_url(self):
        return reverse('client_detail',args=[self.cid,])

class BusinessContact(models.Model):
    # D. BusinessContact: 一个客户公司有多个业务联系人
    bc_id = models.AutoField(primary_key=True)
    bc_name = models.CharField(max_length=50, blank=True, null=True)
    bc_gender = models.CharField(max_length=10,choices=[('M', '男'), ('F', '女'), ('X','未知')], default='X')
    bc_mobile = models.CharField(max_length=50, blank=True, null=True)
    bc_email = models.CharField(max_length=150, blank=True, null=True)
    bc_position = models.CharField(max_length=80, blank=True, null=True)
    cid = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'client_business_contact'

class FinancialContact(models.Model):
    # E. FinancialContact: 一个客户公司有多个财务联系人
    fc_id = models.AutoField(primary_key=True)
    fc_name = models.CharField(max_length=50, blank=True, null=True)
    fc_gender = models.CharField(max_length=10,choices=[('M', '男'), ('F', '女'), ('X','未知')], default='X')
    fc_mobile = models.CharField(max_length=150, blank=True, null=True)
    fc_email = models.CharField(max_length=150, blank=True, null=True)
    pc_position = models.CharField(max_length=80, blank=True, null=True)
    cid = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'client_financial_contact'