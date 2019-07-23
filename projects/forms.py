from django import forms
from .models import *

class FindProjectForm(forms.ModelForm):
    pid = forms.IntegerField(label='项目ID',required=False)
    pname = forms.CharField(label='项目名称',max_length=150,required=False)
    cid = forms.IntegerField(label='客户ID',required=False)
    cname = forms.CharField(label='客户名称',max_length=150,required=False)

    class Meta:
        model = Project
        fields = ('pid','pname','cid','cname')


    def __init__(self, *args, **kwargs):
        super(FindProjectForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})

class ProjectForm(forms.ModelForm):
    pname = forms.CharField(max_length=50,label='项目名称',required=False)
    cid = forms.IntegerField(label='客户ID',required=False)
    pm = forms.CharField(max_length=50,required=False,label='项目经理')
    pm_mobile = forms.CharField(max_length=50,label='项目经理电话',required=False)
    pm_wechat = forms.CharField(max_length=50, label='项目经理微信', required=False)
    pm_email = forms.CharField(max_length=50,label='项目经理邮箱',required=False)
    pm_gender = forms.CharField(max_length=50, label='项目经理性别(M/F)', required=False)
    pdeadline = forms.CharField(max_length=50, label='项目截止日期(YYYY-MM-DD)', required=False)
    premark = forms.CharField(max_length=250, label='备注',required=False)
    pdetail = forms.CharField(max_length=250, label='详情',required=False)
    person_in_charge = forms.CharField(max_length=50,required=False,label='我方项目对接人')
    class Meta:
        model = Project
        fields = ('pname','cid','pm','pm_mobile','pm_wechat','pm_email','pm_gender','pdeadline','premark','pdetail','person_in_charge')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})

class ProjectUpdateForm(forms.ModelForm):
    pname = forms.CharField(max_length=50, label='项目名称', required=False)
    pm = forms.CharField(max_length=50, required=False, label='项目经理')
    #pm_mobile = forms.CharField(max_length=50, label='项目经理电话', required=False)
    #pm_wechat = forms.CharField(max_length=50, label='项目经理微信', required=False)
    #pm_email = forms.CharField(max_length=50, label='项目经理邮箱', required=False)
    pm_gender = forms.CharField(max_length=50, label='项目经理性别(M/F)', required=False)
    pdeadline = forms.CharField(max_length=50, label='项目截止日期(YYYY-MM-DD)', required=False)
    premark = forms.CharField(max_length=250, label='备注',required=False)
    pdetail = forms.CharField(max_length=250, label='详情', required=False)
    person_in_charge = forms.CharField(max_length=50,required=False,label='我方项目对接人')

    class Meta:
        model = Project
        fields = ('pname','pm','pm_gender','pdeadline','premark','pdetail','person_in_charge')
        #fields = ('pname','pm','pm_mobile','pm_wechat','pm_email','pm_gender','pdeadline','premark','pdetail','person_in_charge')

    def __init__(self, *args, **kwargs):
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class": "form-control"})

class PMContactInfoUpdateDB(forms.ModelForm):
    pm_mobile = forms.CharField(max_length=50, label='项目经理电话', required=False)
    pm_wechat = forms.CharField(max_length=50, label='项目经理微信', required=False)
    pm_email = forms.CharField(max_length=50, label='项目经理邮箱', required=False)

    class Meta:
        model = Project
        fields = ('pm_mobile','pm_wechat','pm_email')

    def __init__(self, *args, **kwargs):
        super(PMContactInfoUpdateDB, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class": "form-control"})

class P2EForm(forms.ModelForm):
    # B. Project: 一个项目有多个专家
    # A-B. Project2Experts：多对多
    eid = forms.IntegerField(label='专家ID',required=True)
    ename = forms.CharField(max_length=150, label='专家姓名',required=False)


    class Meta:
        model = Project2Expert
        fields = ('eid','ename')

    def __init__(self, *args, **kwargs):
        super(P2EForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class": "form-control"})


class Project2ExpertForm(forms.ModelForm):
    # B. Project: 一个项目有多个专家
    # A-B. Project2Experts：多对多
    #pid = forms.ForeignKey(Project, on_delete=models.CASCADE)
    #eid = forms.IntegerField(label='专家ID',required=False)
    # 添加的额外字段
    #pname = forms.CharField(max_length=150, label='项目名称',required=False)
    #ename = forms.CharField(max_length=150, label='专家姓名',required=False)
    #ecompany = forms.CharField(max_length=150, label='专家公司',required=False)
    status = forms.IntegerField(label='访谈状态',required=False)
    # datefiled还是charfield？？？
    itv_stime = forms.CharField(label='访谈时间(YYYY-MM-DD Hrs)', required=False)
    itv_duration = forms.IntegerField(label='访谈时长(min)',required=False)

    class Meta:
        model = Project2Expert
        fields = ('status','itv_stime', 'itv_duration')

    def __init__(self, *args, **kwargs):
        super(Project2ExpertForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class": "form-control"})
