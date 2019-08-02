# Create your models here.
from django.db import models
from django.urls import reverse
from django.shortcuts import render
#import os
#import xlsxwriter

class ExpertInfo(models.Model):
    eid = models.AutoField(primary_key=True)
    ename = models.CharField(max_length=150, blank=True, null=True)
    esex = models.CharField(max_length=10, choices=[('M', '男'), ('F', '女'), ('X','未知')], default='X')
    emobile = models.CharField(max_length=150, blank=True, null=True)
    eemail = models.CharField(max_length=150, blank=True, null=True)
    etrade = models.CharField(max_length=150, blank=True, null=True)
    esubtrade = models.CharField(max_length=150, blank=True, null=True)
    elocation = models.CharField(max_length=150, blank=True, null=True)
    eqq = models.CharField(max_length=150, blank=True, null=True)
    estate = models.IntegerField(blank=True, null=True)
    ecomefrom = models.TextField(blank=True, null=True)
    eremark = models.TextField(blank=True, null=True)
    addtime = models.DateTimeField(auto_now_add=True)
    ebackground = models.TextField(blank=True, null=False)
    efee = models.FloatField(blank=True,null=False,default=0.0,verbose_name='专家付费单价')
    eupdated_by = models.CharField(max_length=150, blank=True, null=True)
    interview_num = models.IntegerField(blank=True,null=True,default=0)

    class Meta:
        managed = True
        ordering = ('-addtime',)
        db_table = 'expert_info'
    def __str__(self):
        return "{}-{}".format(self.eid, self.ename)

    def contact_info(self):
        print("==============models.contact_info============", self.ename,self.eid)
        #print(reverse('expert_contact_info', args=[self.eid]))
        return reverse('expert_contact_info', args=[self.ename,self.eid])

    def expert_contact_info_update(self):
        print("==============models.expert_contact_info_update============", self.ename, self.eid)
        return reverse('expert_contact_info_update', args=[self.ename, self.eid])

    def myDelete(self):
        print("==============models.delete============",self.eid, self.ename)
        return reverse('myDelete',args=[self.eid, self.ename])

    def delete_confirm_url(self):
        print("==============models.delete_confirm_url============",self.eid, self.ename)
        return reverse('delete_confirm',args=[self.eid, self.ename])

    def get_absolute_url(self):
        return reverse('expert_detail',args=[self.ename, self.eid])

    def get_comment_url(self):
        print("==============models.get_comment_url============",self.eid, self.ename)
        return reverse('comment_detail',args=[self.eid, self.ename])

    def add_comment_url(self):
        return reverse('add_comment',args=[self.eid,self.ename])

    def get_workexp_url(self):
        print("==============models.get_workexp_url============", self.eid, self.ename)
        return reverse('workexp_detail',args=[self.eid, self.ename])

    def add_workexp_url(self):
        return reverse('add_workexp',args=[self.eid,self.ename])

    def get_update_url(self):
        return reverse('expert_detail_update', args=[self.ename, self.eid])

    def get_company(self):
        #print("==============models.get_workexp============")
        work_list = WorkExp.objects.filter(eid=self.eid)
        if len(work_list) == 0:
            return "无"
        else:
            #l = [work_list[0].company, work_list[0].position]
            #return ('-').join(l)
            #result = ('；').join([(work.company,work.position).__str__() for work in work_list])
            return work_list[0].company

    def get_position(self):
        #print("==============models.get_workexp============")
        work_list = WorkExp.objects.filter(eid=self.eid)
        if len(work_list) == 0:
            return "无"
        else:
            #l = [work_list[0].company,work_list[0].position]
            return work_list[0].position
            #result = ('；').join([work.position for work in work_list])
            #return result

    def get_duty(self):
        #print("==============models.get_workexp============")
        work_list = WorkExp.objects.filter(eid=self.eid)
        if len(work_list) == 0:
            return "无"
        else:
            #l = [work_list[0].company,work_list[0].position]
            return work_list[0].duty
            #result = ('；').join([work.position for work in work_list])
            #return result


class ExpertComments(models.Model):

    cmtid = models.AutoField(primary_key=True)
    eid = models.ForeignKey('ExpertInfo', models.DO_NOTHING, db_column='eid')
    eproblem = models.TextField(blank=True, null=True)
    ecomment = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'expert_comments'

    def __str__(self):
        # 默认的人们可读的对象表达方式
        return "{}-{}".format(self.eid,self.eproblem)


    # 刚加的
    def get_comment_update_url(self):
        print("==========在models.py中的 get_comment_update_url()")
        num = self.eid.eid
        #print(type(num))
        return reverse('comment_detail_update', args=[num,self.cmtid ])

    def delete_comment(self):
        print("==========在models.py中的 delete_comment()")
        num = self.eid.eid
        #print(type(num))
        return reverse('delete_comment', args=[num,self.cmtid ])

    def delete_comment_confirm(self):
        print("==========在models.py中的 delete_comment_confirm()")
        num = self.eid.eid
        #print(type(num))
        return reverse('delete_comment_confirm', args=[num,self.cmtid ])
    """
    def get_comment_url(self):
        return reverse('comment_detail',args=[self.eid,])
    """

class WorkExp(models.Model):
    expid = models.AutoField(primary_key=True)
    eid = models.ForeignKey(ExpertInfo, models.DO_NOTHING, db_column='eid')
    stime = models.CharField(max_length=150,blank=True, null=True)
    etime = models.CharField(max_length=150,blank=True, null=True)
    company = models.CharField(max_length=250, blank=True, null=True)
    agency = models.CharField(max_length=150, blank=True, null=True)
    position = models.CharField(max_length=150, blank=True, null=True)
    duty = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        ordering = ('-stime',)
        db_table = 'work_exp'

    def __str__(self):
        return "{}-{}".format(self.company,self.position)

    def get_workexp_update_url(self):
        #print("==========在models.py中的 get_workexp_update_url()")
        num = self.eid.eid
        return reverse('workexp_detail_update', args=[num, self.expid])

    def delete_workexp(self):
        #print("==========在models.py中的 delete_workexp()")
        num = self.eid.eid
        return reverse('delete_workexp', args=[num, self.expid])

    def delete_workexp_confirm(self):
        #print("==========在models.py中的 delete_workexp_confirm()")
        num = self.eid.eid
        return reverse('delete_workexp_confirm', args=[num, self.expid])


class Payment(models.Model):
    # F. Expert_Payment
    ep_id = models.AutoField(primary_key=True)
    eid = models.ForeignKey(ExpertInfo, on_delete=models.CASCADE)
    alipay = models.CharField(max_length=150, blank=True, null=True, verbose_name='支付宝')
    bank = models.CharField(max_length=250, blank=True, null=True, verbose_name='银行账号')
    wechat = models.CharField(max_length=150, blank=True, null=True, verbose_name='微信支付')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')

    class Meta:
        managed = True
        db_table = 'payment'

    def __str__(self):
        return "{}-{}".format(self.ep_id,self.eid)

    def get_payment_update(self):
        print("==========在models.py中的 get_payment_update()")

        return reverse('get_payment_update', args=[self.ep_id,])

