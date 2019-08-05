from django import forms
from .models import ExpertInfo,ExpertComments,WorkExp,Payment
#import datetime

# 从ExpertInfo模型中动态地创建表单
class ExpertInfoForm(forms.ModelForm):
    ename = forms.CharField(label='姓名',required=True)
    esex = forms.CharField(label='性别',required=False)
    emobile = forms.CharField(label='电话',required=True)
    eemail = forms.CharField(label='邮箱',required=False)
    etrade = forms.CharField(label='行业',required=False)
    esubtrade = forms.CharField(label='子行业',required=False)

    elocation = forms.CharField(label='城市',required=False)
    eqq = forms.CharField(label='微信',required=False)
    estate = forms.IntegerField(label='级别',required=False)
    ecomefrom = forms.CharField(label='来源',required=False)
    eremark = forms.CharField(label='备注',required=False)
    ebackground = forms.CharField(label='背景',required=False)
    efee = forms.FloatField(label='咨询费',required=False)
    interview_num = forms.IntegerField(label='访谈次数',required=False)
    eupdated_by = forms.CharField(label='录入员工姓名',required=True)


    class Meta:
        model = ExpertInfo
        fields = ('ename','esex','emobile','eemail','etrade',
                  'esubtrade','elocation',
                  'eqq','estate','ecomefrom','eremark','ebackground','efee','interview_num','eupdated_by')

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
    eproblem = forms.CharField(label='问题',required=False)
    ecomment = forms.CharField(label='回答',required=False)


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
    stime = forms.CharField(label='开始时间',required=True)
    etime = forms.CharField(label='结束时间',required=False)
    company = forms.CharField(label='公司',required=True)
    agency = forms.CharField(label='部门',required=False)
    position = forms.CharField(label='职位',required=False)
    duty = forms.CharField(label='职责',required=False)
    area = forms.CharField(label='领域',required=False)


    class Meta:
        model = WorkExp
        fields = ('company', 'agency', 'position','area','stime', 'etime','duty')
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

class PaymentForm(forms.ModelForm):
    # F. Expert_Payment
    alipay = forms.CharField(label='支付宝',required=False)
    bank = forms.CharField(label='银行账号',required=False)
    wechat = forms.CharField(label='微信支付',required=False)
    remark = forms.CharField(label='备注',required=False)

    class Meta:
        model = Payment
        fields = ['alipay','bank','wechat','remark']

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            print(field_name)
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})