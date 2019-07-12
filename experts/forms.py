from django import forms
from .models import ExpertInfo,ExpertComments,WorkExp
#import datetime

# 从ExpertInfo模型中动态地创建表单
class ExpertInfoForm(forms.ModelForm):
    ename = forms.CharField(label='*姓名',max_length=50, required=True)
    esex = forms.CharField(label='性别(M/F)',max_length=2, required=False)
    emobile = forms.CharField(label='*电话(多个电话请用分号隔开)',max_length=50, required=True)
    eemail = forms.CharField(label='邮箱',max_length=80, required=False)
    etrade = forms.CharField(label='行业',max_length=150, required=False)
    esubtrade = forms.CharField(label='子行业',max_length=150, required=False)
    ebirthday = forms.DateField(label='生日',required=False)
    #elandline = forms.CharField(max_length=50, required=False)
    elocation = forms.CharField(label='城市',max_length=150, required=False)
    eqq = forms.CharField(label='微信',max_length=50, required=False)
    #ephoto = forms.CharField(max_length=20, required=False)
    estate = forms.IntegerField(label='级别',required=False)
    ecomefrom = forms.CharField(label='来源',required=False)
    eremark = forms.CharField(label='备注',required=False)
    ebackground = forms.CharField(label='背景',required=False)
    efee = forms.FloatField(label='咨询费',required=False)
    #admin_id = forms.IntegerField(required=False)
    #addtime = forms.DateTimeField(initial=datetime.now())

    class Meta:
        model = ExpertInfo
        fields = ('ename','esex','emobile','eemail','etrade',
                  'esubtrade','ebirthday','elocation',
                  'eqq','estate','ecomefrom','eremark','ebackground','efee')

    def __init__(self, *args, **kwargs):
        super(ExpertInfoForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})


# 从ExpertInfo模型中动态地创建表单
class CommentForm(forms.ModelForm):

    #ename = forms.CharField(max_length=50, required=True)
    #emobile = forms.CharField(max_length=50, required=True)
    #allExperts = ExpertInfo.objects.all()

    #for exp in allExperts:
    #    if(exp.ename==ename and exp.emobile==emobile):
    #        eid = exp.eid
    eproblem = forms.CharField(label='问题',required=True)
    ecomment = forms.CharField(label='回答',required=True)


    class Meta:
        model = ExpertComments
        fields = ('eproblem', 'ecomment')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})



# 从ExpertInfo模型中动态地创建表单
class WorkexpForm(forms.ModelForm):
    # ename = forms.CharField(max_length=50, required=True)
    # emobile = forms.CharField(max_length=50, required=True)
    # allExperts = ExpertInfo.objects.all()
    # for exp in allExperts:
    #     if(exp.ename==ename and exp.emobile==emobile):
    #         eid = exp.eid
    stime = forms.CharField(label='*开始时间(YYYY-MM)',required=True)
    etime = forms.CharField(label='结束时间(YYYY-MM)',required=False)
    company = forms.CharField(label='公司',max_length=150,required=False)
    agency = forms.CharField(label='部门',max_length=150,required=False)
    position = forms.CharField(label='职位',max_length=150,required=False)
    duty = forms.CharField(label='职责',max_length=150,required=False)
    area = forms.CharField(label='领域',max_length=150,required=False)


    class Meta:
        model = WorkExp
        fields = ('stime', 'etime','company', 'agency', 'position', 'duty','area')
        #fields = ('ename','emobile','stime','etime',
        #          'company','agency','position','duty',
        #          'area','istonow')

    def __init__(self, *args, **kwargs):
        super(WorkexpForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})

class deleteConfirmForm(forms.Form):
    ename = forms.CharField(required=True)
    eid = forms.IntegerField(required=True)
    class Meta:
        model = ExpertInfo
        fields = ['ename','eid']

    def __init__(self, *args, **kwargs):
        super(deleteConfirmForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            print(field_name)
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})