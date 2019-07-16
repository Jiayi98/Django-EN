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
    cname = forms.CharField(max_length=50,label='项目名称',required=False)
    bc = forms.CharField(max_length=50,required=False,label='主业务联系人')
    fc = forms.CharField(max_length=50,label='主财务联系人',required=False)
    ctype = forms.CharField(max_length=50,label='客户类型',required=False)
    cinfo = forms.CharField(max_length=10, label='客户信息', required=False)
    half_hrs = forms.IntegerField(label='半小时政策',required=False)

    class Meta:
        model = Client
        fields = ('cname','cid','bc','fc','ctype','cinfo','half_hrs')

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})
