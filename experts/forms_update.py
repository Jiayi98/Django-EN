from django import forms
from .models import ExpertInfo,ExpertComments,WorkExp


# 从ExpertInfo模型中动态地创建表单
class ExpertInfoFormUpdate(forms.ModelForm):
    ename = forms.CharField(required=False)

    class Meta:
        model = ExpertInfo
        fields = ('ename',)


    def __init__(self, *args, **kwargs):
        super(ExpertInfoFormUpdate, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})

class ExpertInfoFormUpdateDB(forms.ModelForm):
    ename = forms.CharField(label='姓名', required=False)
    esex = forms.CharField(label='性别', required=False)
    etrade = forms.CharField(label='行业', required=False)
    esubtrade = forms.CharField(label='子行业', required=False)
    elocation = forms.CharField(label='地区', required=False)
    estate = forms.IntegerField(label='评级',required=False)
    ecomefrom = forms.CharField(label='来源',required=False)
    eremark = forms.CharField(label='备注',required=False)
    efee = forms.FloatField(label='咨询费', required=False)
    ebackground = forms.CharField(label='背景',required=False)
    interview_num = forms.IntegerField(label='访谈次数',required=False)
    eupdated_by = forms.CharField(label='修改员工姓名', required=False)


    class Meta:
        model = ExpertInfo
        fields = ('ename','esex','etrade',
                  'esubtrade','elocation',
                  'estate','ecomefrom','eremark','efee','ebackground','interview_num','eupdated_by')

    def __init__(self, *args, **kwargs):
        super(ExpertInfoFormUpdateDB, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})

class ContactInfoFormUpdateDB(forms.ModelForm):
    #ename = forms.CharField(label='姓名',max_length=50, required=True)

    emobile = forms.CharField(label='电话', required=False)
    eemail = forms.CharField(label='邮箱', required=False)
    eqq = forms.CharField(label='微信', required=False)
    eupdated_by = forms.CharField(label='修改人', required=False)

    class Meta:
        model = ExpertInfo
        fields = ('emobile','eemail','eqq','eupdated_by')

    def __init__(self, *args, **kwargs):
        super(ContactInfoFormUpdateDB, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})

#刚加的

class CommentFormUpdateDB(forms.ModelForm):
    eproblem = forms.CharField(label='问题',required=False)
    ecomment = forms.CharField(label='回答',required=False)

    class Meta:
        model = ExpertComments
        fields = ('eproblem','ecomment')

    def __init__(self, *args, **kwargs):
        super(CommentFormUpdateDB, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})


class WorkexpFormUpdateDB(forms.ModelForm):
    stime = forms.CharField(label='开始时间',required=True)
    etime = forms.CharField(label='结束时间',required=False)
    company = forms.CharField(label='公司',required=False)
    agency = forms.CharField(label='部门', required=False)
    position = forms.CharField(label='职位', required=False)
    duty = forms.CharField(label='职责',required=False)
    area = forms.CharField(label='领域', required=False)

    class Meta:
        model = WorkExp
        fields = ('company','agency','position','area','stime','etime','duty')

    def __init__(self, *args, **kwargs):
        super(WorkexpFormUpdateDB, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})
            
