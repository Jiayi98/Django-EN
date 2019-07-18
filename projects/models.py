from django.db import models
from experts.models import ExpertInfo
from clients.models import Client
from django.urls import reverse

# Create your models here.
class Project(models.Model):
    # B. Project: 一个项目有多个专家,一个专家参与多个项目
    pid = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=50, blank=True, null=True, verbose_name='项目名称')
    cid = models.ForeignKey(Client, on_delete=models.CASCADE, to_field='cid')
    cname = models.CharField(max_length=150, blank=True, null=True, verbose_name='客户名称')
    pm = models.CharField(max_length=50, blank=True, null=True, verbose_name='项目经理')
    pm_mobile = models.CharField(max_length=50, blank=True, null=True)
    pm_email = models.CharField(max_length=150, blank=True, null=True)
    pm_gender = models.CharField(max_length=50,choices=[('M', '男'), ('F', '女'), ('X','未知')], default='X')
    pcreatetime = models.DateField(auto_now_add=True)
    pdeadline = models.CharField(max_length=50, blank=True, null=True)
    premark = models.TextField(blank=True,null=True)
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
        print("==========projects/models.add_p2e")
        return reverse('add_p2e',args=[self.pid,])

    def update_project_detail(self):
        print("==========projects/models.update_project_detail========")
        return reverse('update_project_detail', args=[self.pid,])

class Project2Expert(models.Model):
    # B. Project: 一个项目有多个专家
    # A-B. Project2Experts：多对多
    pteid = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Project, on_delete=models.CASCADE)
    eid = models.ForeignKey(ExpertInfo, on_delete=models.CASCADE)
    # 添加的额外字段
    pname = models.CharField(max_length=150, blank=True, null=True, verbose_name='项目名称')
    ename = models.CharField(max_length=50, blank=True, null=True, verbose_name='专家姓名')
    ecompany = models.CharField(max_length=150, blank=True, null=True, verbose_name = '专家公司')
    status = models.IntegerField(choices=[(1, '已访谈'), (0, '未访谈')], default=0, verbose_name='访谈状态')
    # datefiled还是charfield？？？
    itv_stime = models.CharField(max_length=50, blank=True, null=True, verbose_name='访谈时间')
    itv_duration = models.IntegerField(blank=True, null=False, default=0, verbose_name='访谈时常')

    class Meta:
        managed = True
        db_table = 'p_e_relationship'
        unique_together = ('pid', 'eid')

    def __str__(self):
        return "{}-{}".format(self.pname,self.ename)

    def update_p2e_url(self):
        print("==========projects/models.update_p2e_url()")
        return reverse('update_p2e_detail', args=[self.pteid,])