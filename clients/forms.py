from django import forms
from .models import *

class FindClientForm(forms.ModelForm):
    id = forms.IntegerField(label='客户ID',required=False)
    cname = forms.CharField(label='客户名称',max_length=150,required=False)
    #bc = forms.IntegerField(label='客户ID',required=False)
    #fc = forms.IntegerField(label='客户ID',required=False)

    class Meta:
        model = Client
        fields = ('cid','cname')


    def __init__(self, *args, **kwargs):
        super(FindClientForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})

class ClientForm(forms.ModelForm):
    cname = forms.CharField(max_length=50,label='客户名称',required=False)
    bc_name = forms.CharField(max_length=50,required=False,label='主业务联系人')
    fc_name = forms.CharField(max_length=50,label='主财务联系人',required=False)
    ctype = forms.CharField(max_length=50,label='客户类型',required=False)
    cinfo = forms.CharField(label='客户信息', required=False)
    half_hrs = forms.IntegerField(label='半小时政策',required=False)

    class Meta:
        model = Client
        fields = ('cname','bc_name','fc_name','ctype','cinfo','half_hrs')

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})

class BCForm(forms.ModelForm):
    bc_name = forms.CharField(label='业务联系人姓名',max_length=50, required=False)
    bc_gender = forms.CharField(label='业务联系人性别(M/F)',max_length=10, required=False)
    bc_mobile = forms.CharField(label='业务联系人电话',max_length=50, required=False)
    bc_email = forms.CharField(label='业务联系人邮箱',max_length=50, required=False)
    bc_position = forms.CharField(label='业务联系人职位',max_length=50, required=False)

    class Meta:
        model = BusinessContact
        fields = ('bc_name','bc_gender','bc_mobile','bc_email','bc_position')

    def __init__(self, *args, **kwargs):
        super(BCForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})


class FCForm(forms.ModelForm):
    fc_name = forms.CharField(label='财务联系人姓名',max_length=50, required=False)
    fc_gender = forms.CharField(label='财务联系人性别(M/F)',max_length=10, required=False)
    fc_mobile = forms.CharField(label='财务联系人电话',max_length=50, required=False)
    fc_email = forms.CharField(label='财务联系人邮箱',max_length=50, required=False)
    fc_position = forms.CharField(label='财务联系人职位',max_length=50, required=False)

    class Meta:
        model = FinancialContact
        fields = ('fc_name','fc_gender','fc_mobile','fc_email','fc_position')

    def __init__(self, *args, **kwargs):
        super(FCForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})