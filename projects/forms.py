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
    pm_email = forms.CharField(max_length=50,label='项目经理邮箱',required=False)
    pm_gender = forms.CharField(max_length=10, label='项目经理性别(M/F)', required=False)
    pdeadline = forms.CharField(max_length=50, label='项目截止日期(YYYY-MM-DD)', required=False)

    class Meta:
        model = Project
        fields = ('pname','cid','pm','pm_mobile','pm_email','pm_gender','pdeadline')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})
