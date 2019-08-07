from django import forms
from .models import *

class FindProjectForm(forms.ModelForm):
    pid = forms.IntegerField(label='项目ID',required=False)
    pname = forms.CharField(label='项目名称',required=False)
    cid = forms.IntegerField(label='客户ID',required=False)
    cname = forms.CharField(label='客户名称',required=False)

    class Meta:
        model = Project
        fields = ('pid','pname','cid','cname')


    def __init__(self, *args, **kwargs):
        super(FindProjectForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})

class ProjectForm(forms.ModelForm):
    # 该表单用于添加项目信息
    pname = forms.CharField(label='项目名称',required=False)
    cid = forms.IntegerField(label='客户ID',required=False)
    pm = forms.CharField(required=False,label='客户对接人')
    pcreatetime = forms.CharField(label='开始日期(YYYY-MM-DD)', required=False)
    pdeadline = forms.CharField(label='结束日期(YYYY-MM-DD)', required=False)
    premark = forms.CharField(label='备注',required=False)
    pdetail = forms.CharField(label='详情',required=False)
    person_in_charge = forms.CharField(required=False,label='项目经理')
    class Meta:
        model = Project
        fields = ('pname','cid','pm','pcreatetime','pdeadline','premark','pdetail','person_in_charge')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})

class ProjectUpdateForm(forms.ModelForm):
    # 该表单用于更新项目信息
    pname = forms.CharField(label='项目名称', required=False)
    pm = forms.CharField(required=False, label='客户项目经理')
    pcreatetime = forms.CharField(label='开始日期(YYYY-MM-DD)', required=False)
    pdeadline = forms.CharField(label='项目截止日期(YYYY-MM-DD)', required=False)
    premark = forms.CharField(label='备注',required=False)
    pdetail = forms.CharField(label='详情', required=False)
    person_in_charge = forms.CharField(required=False,label='我方项目对接人')

    class Meta:
        model = Project
        fields = ('pname','pm','person_in_charge','pcreatetime','pdeadline','premark','pdetail')

    def __init__(self, *args, **kwargs):
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class": "form-control"})



class P2EForm(forms.ModelForm):
    # 该表单用于添加访谈时查询专家
    eid = forms.IntegerField(label='专家ID',required=True)
    ename = forms.CharField(label='专家姓名',required=False)


    class Meta:
        model = Project2Expert
        fields = ('eid','ename')

    def __init__(self, *args, **kwargs):
        super(P2EForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class": "form-control"})


class Project2ExpertForm(forms.ModelForm):
    # 该表单用于添加/更新p_e_relationship表中的单条访谈记录
    status = forms.IntegerField(label='访谈状态',required=False)
    itv_date = forms.CharField(label='访谈日期', required=False)
    itv_stime = forms.CharField(label='开始时间', required=False)
    itv_etime = forms.CharField(label='结束时间', required=False)
    itv_duration = forms.IntegerField(label='访谈时长(min)',required=False)
    itv_paid_duration = forms.IntegerField(label='计费时长(min)',required=False)
    recorder = forms.CharField(label='录入人',required=False)
    interviewer = forms.CharField(label='约谈人',required=False)
    fee_index = forms.FloatField(label='咨费系数',required=False)
    knowledge = forms.IntegerField(label='知识范围',required=False)
    communication = forms.IntegerField(label='沟通能力',required=False)
    cooperation = forms.IntegerField(label='配合程度',required=False)
    itv_approach = forms.CharField(label='咨询方式',required=False)

    class Meta:
        model = Project2Expert
        fields = ('status','itv_date','itv_stime', 'itv_etime','itv_approach','itv_duration','itv_paid_duration', 'knowledge','communication','cooperation','fee_index', 'interviewer', 'recorder')

    def __init__(self, *args, **kwargs):
        super(Project2ExpertForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class": "form-control"})
