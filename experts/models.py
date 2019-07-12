# Create your models here.
from django.db import models
from django.urls import reverse
from django.shortcuts import render
#import os
#import xlsxwriter

class ExpertInfo(models.Model):
    eid = models.AutoField(primary_key=True)
    ename = models.CharField(max_length=50)
    esex = models.CharField(max_length=2)
    emobile = models.CharField(max_length=50, blank=True, null=True)
    eemail = models.CharField(max_length=80, blank=True, null=True)
    etrade = models.CharField(max_length=150, blank=True, null=True)
    esubtrade = models.CharField(max_length=150, blank=True, null=True)
    ebirthday = models.DateField(blank=True, null=True)
    elandline = models.CharField(max_length=50, blank=True, null=True)
    elocation = models.CharField(max_length=150, blank=True, null=True)
    emsn = models.CharField(max_length=80, blank=True, null=True)
    eqq = models.CharField(max_length=50, blank=True, null=True)
    ephoto = models.CharField(max_length=20, blank=True, null=True)
    estate = models.IntegerField(blank=True, null=True)
    ecomefrom = models.TextField(blank=True, null=True)
    eremark = models.TextField(blank=True, null=True)
    admin_id = models.IntegerField(blank=True, null=True)
    addtime = models.DateTimeField(auto_now_add=True)
    ebackground = models.TextField(blank=True, null=False)
    efee = models.FloatField(blank=True,null=False,default=0.0)

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
        return reverse('add_comment',args=[self.ename, self.emobile])

    def get_workexp_url(self):
        print("==============models.get_workexp_url============", self.eid, self.ename)
        return reverse('workexp_detail',args=[self.eid, self.ename])

    def add_workexp_url(self):
        return reverse('add_workexp',args=[self.ename, self.emobile])

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
    """
    def export_excel(self):
        print("=============models.export_excel========")
        par_path = '/Users/user/Django/mysite/experts/static/xlsxfiles'
        os.chdir(par_path)
        file = 'all_poemers.xlsx'
        if os.path.isfile(file):
            os.remove(file)
            data = self.all_experts_data()

        fields = ['ename','esex','emobile','eemail','etrade',
                  'esubtrade','ebirthday','elocation',
                  'eqq','estate','ecomefrom','eremark','efee','ebackground']
        workbook = xlsxwriter.Workbook(file,encoding='utf-8')
        worksheet = workbook.add_worksheet('data')
        # 表头格式
        format1 = workbook.add_format(
            {'bold': True, 'font_color': 'black', 'font_size': 13, 'align': 'left', 'font_name': u'宋体'})
        # 表头外格式
        format2 = workbook.add_format({'font_color': 'black', 'font_size': 9, 'align': 'left', 'font_name': u'宋体'})
        # A列列宽设置能更好的显示
        worksheet.set_column("A:A", 9)
        # 插入第一行表头标题
        for i in range(0, len(fields)):
            field = fields[i]
            worksheet.write(0, i, field, format1)
        # 从第二行开始插入数据
        for i in range(len(data)):
            item = data[i]
            for j in range(len(fields)):
                field = fields[j]
                worksheet.write(i + 1, j, item[field], format2)
        workbook.close()
        alert_text = '导出%s条数据到excel成功' % len(data)
        return alert_text
    """


class ExpertComments(models.Model):
    """
    cmtid = models.AutoField(primary_key=True)
    eid = models.ForeignKey('ExpertInfo', on_delete=models.CASCADE)
    #eid = models.ForeignKey('ExpertInfo', models.DO_NOTHING, db_column='eid')
    eproblem = models.TextField(blank=True, null=True)
    ecomment = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        #db_table = expert_comments
    """
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
        print(type(num))
        return reverse('comment_detail_update', args=[num,self.cmtid ])

    def delete_comment(self):
        print("==========在models.py中的 delete_comment()")
        num = self.eid.eid
        print(type(num))
        return reverse('delete_comment', args=[num,self.cmtid ])

    def delete_comment_confirm(self):
        print("==========在models.py中的 delete_comment_confirm()")
        num = self.eid.eid
        print(type(num))
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
    company = models.CharField(max_length=150, blank=True, null=True)
    agency = models.CharField(max_length=150, blank=True, null=True)
    position = models.CharField(max_length=150, blank=True, null=True)
    duty = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    istonow = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        ordering = ('-stime',)
        db_table = 'work_exp'

    def __str__(self):
        return "{}-{}".format(self.company,self.position)

    def get_workexp_update_url(self):
        print("==========在models.py中的 get_workexp_update_url()")
        num = self.eid.eid
        return reverse('workexp_detail_update', args=[num, self.expid])

    def delete_workexp(self):
        print("==========在models.py中的 delete_workexp()")
        num = self.eid.eid
        return reverse('delete_workexp', args=[num, self.expid])

    def delete_workexp_confirm(self):
        print("==========在models.py中的 delete_workexp_confirm()")
        num = self.eid.eid
        return reverse('delete_workexp_confirm', args=[num, self.expid])

"""
class WorkExp(models.Model):
    expid = models.AutoField(primary_key=True)
    eid = models.ForeignKey('ExpertInfo', on_delete=models.CASCADE)
    #eid = models.ForeignKey(ExpertInfo, models.DO_NOTHING, db_column='eid')
    stime = models.DateField(blank=True, null=True)
    etime = models.DateField(blank=True, null=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    agency = models.CharField(max_length=150, blank=True, null=True)
    position = models.CharField(max_length=150, blank=True, null=True)
    duty = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    istonow = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        ordering = ('-stime',)
        #db_table = work_exp

    def __str__(self):
        return "{}-{}".format(self.eid,self.company)

    def get_workexp_update_url(self):
        print("==========在models.py中的 get_workexp_update_url()")
        num = self.eid.eid
        print(type(num))
        return reverse('workexp_detail_update', args=[num,self.expid])

    def delete_workexp(self):
        print("==========在models.py中的 delete_workexp()")
        num = self.eid.eid
        print(type(num))
        return reverse('delete_workexp', args=[num,self.expid])

    def delete_workexp_confirm(self):
        print("==========在models.py中的 delete_workexp_confirm()")
        num = self.eid.eid
        print(type(num))
        return reverse('delete_workexp_confirm', args=[num,self.expid])
"""