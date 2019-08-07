from django.db import models
from experts.models import ExpertInfo
from clients.models import Client
from django.urls import reverse


# Create your models here.
class Project(models.Model):
    # B. Project: 一个项目有多个专家,一个专家参与多个项目
    pid = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=250, blank=True, null=True, verbose_name='项目名称')
    cid = models.ForeignKey(Client, on_delete=models.CASCADE, to_field='cid')
    pm = models.CharField(max_length=150, blank=True, null=True, verbose_name='项目经理')
    pcreatetime = models.CharField(max_length=150, blank=True, null=True)
    pdeadline = models.CharField(max_length=150, blank=True, null=True)
    premark = models.TextField(blank=True,null=True)
    pdetail = models.TextField(blank=True,null=True)
    person_in_charge = models.CharField(max_length=150, blank=True, null=True, verbose_name='我方项目对接人')
    expertinfos = models.ManyToManyField(ExpertInfo, through='Project2Expert')

    class Meta:
        managed = True
        ordering = ('-pcreatetime','pdeadline')
        db_table = 'project_info'


    def __str__(self):
        return "{}-{}".format(self.pid, self.pname)

    def get_project_detail(self):
        return reverse('project_detail',args=[self.pid,self.cid.cid])

    def add_p2e(self):
        #print("==========projects/models.add_p2e")
        return reverse('add_p2e',args=[self.pid,])

    def update_project_detail(self):
        #print("==========projects/models.update_project_detail========")
        return reverse('update_project_detail', args=[self.pid,])

    def delete_project(self):
        return reverse('delete_project', args=[self.pid,])

    def pm_contact_info_update(self):
        return reverse('pm_contact_info_update', args=[self.pid,])

    def get_client_name(self):
        return self.cid.cname


class Project2Expert(models.Model):
    # 访谈信息表
    # B. Project: 一个项目有多个专家
    # A-B. Project2Experts：多对多
    pteid = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Project, on_delete=models.CASCADE)
    eid = models.ForeignKey(ExpertInfo, on_delete=models.CASCADE)
    status = models.IntegerField(choices=[(1, '已访谈'), (0, '未访谈')], default=0, verbose_name='访谈状态')
    itv_date = models.CharField(max_length=150, blank=True, null=True, verbose_name='访谈日期')
    itv_stime = models.CharField(max_length=150, blank=True, null=True, verbose_name='开始时间')
    itv_etime = models.CharField(max_length=150, blank=True, null=True, verbose_name='结束时间')
    itv_duration = models.IntegerField(blank=True, null=False, default=0, verbose_name='访谈时长')
    itv_paid_duration = models.IntegerField(blank=True, null=False, default=0, verbose_name='计费时长')
    recorder = models.CharField(max_length=150, blank=True, null=True, verbose_name='录入人')
    interviewer = models.CharField(max_length=150, blank=True, null=True, verbose_name='约谈人')
    e_payment = models.FloatField(blank=True,null=False,default=0.0,verbose_name='专家付费总额')
    c_payment = models.FloatField(blank=True,null=False,default=0.0,verbose_name='客户收费总额')
    fee_index = models.FloatField(blank=True,null=False,default=1.0,verbose_name='咨费系数')
    knowledge = models.IntegerField(blank=True, null=False, default=0, verbose_name='知识范围')
    communication = models.IntegerField(blank=True, null=False, default=0, verbose_name='沟通能力')
    cooperation = models.IntegerField(blank=True, null=False, default=0, verbose_name='配合程度')
    avg_score = models.FloatField(blank=True,null=False,default=0.0,verbose_name='均分')
    itv_approach = models.CharField(max_length=150, blank=True, null=True, verbose_name='咨询方式')

    class Meta:
        managed = True
        ordering = ('-itv_date', '-itv_stime',)
        db_table = 'p_e_relationship'


    def __str__(self):
        return "{}-{}".format(self.pname,self.ename)

    def update_p2e_url(self):
        #print("==========projects/models.update_p2e_url()")
        return reverse('update_p2e_detail', args=[self.pteid,])

    def get_expert_company(self):
        # 返回最近一条工作经历的公司名
        return self.eid.get_company()

