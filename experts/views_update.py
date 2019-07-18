# Create your views here.
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import ExpertInfo,ExpertComments,WorkExp
#from .forms import ExpertInfoForm, CommentForm,WorkexpForm
from .forms_update import ExpertInfoFormUpdate,ContactInfoFormUpdateDB
#CommentFormUpdate,WorkexpFormUpdate,ExpertInfoFormUpdateDB
from django.contrib.auth.decorators import login_required
from .views import comment_detail
from django.db import transaction
from django.contrib.auth.decorators import permission_required

@login_required
#@permission_required('experts.can_delete_expert_info')
def expertInfoDelete(request):
    #print("============用到了这个吗==========")
    form = ExpertInfoFormUpdate()
    return render(request, 'experts/delete_expert.html',{'form': form})

@login_required
@transaction.atomic
def expertInfoDeleteFromDatabase(request):
    #print("!!!!!!!!!!!views.update.DELETE这里！!!!!!!!!")
    form = ExpertInfoFormUpdate()
    ename = request.POST["ename"]
    expert_objs = ExpertInfo.objects.filter(ename=ename)
    for obj in expert_objs:
        print(obj.eid)

    return render(request, 'experts/delete_expert.html', {'form': form,'expert_objs': expert_objs})


"""
更新专家个人信息，对应的是ExpertInfo这个model
"""
@login_required
def expertInfoUpdate(request):
    #print("============用到了这个吗==========")
    # ExpertInfoFormUpdate 是一个用于输入被修改的专家的姓名的表单，只有ename一个字段
    form = ExpertInfoFormUpdate()
    return render(request, 'experts/update_expert.html',{'form': form})



@login_required
@transaction.atomic
def expertInfoUpdateToDatabase(request):
    #print("!!!!!!!!!!!UPDATE这里！!!!!!!!!")
    form = ExpertInfoFormUpdate()
    ename = request.POST["ename"]
    expert_objs = ExpertInfo.objects.filter(ename=ename)
    # 找到所有同名的专家
    #for obj in expert_objs:
    #    print(obj.eid)
    # 在update_expert.html中：
    # <form action="/expertinfoupdatetodatabase/" class="form-horizontal" method="post" name="expertinfoupdatetodatabase">
    # 选择某一专家后调用该object的【def expert_detail_update()】来更新具体信息。
    # 更新信息的form【ExpertInfoFormUpdateDB】所对应的view在view.expert_detail_update()中
    return render(request, 'experts/update_expert.html', {'form': form,'expert_objs': expert_objs})

# 6.24

@login_required
def delete_comment(request, eid, cmtid):
    print("=============views_update.delete_comment======")
    template_name = 'experts/comment_detail.html'
    result = {}
    try:
        #print("==============Try========")
        expert = ExpertInfo.objects.get(eid=eid)
        c = ExpertComments.objects.get(cmtid=cmtid)
    except:
        #print("==============ERROR========")
        result['status'] = 'error'
    else:
        result['status'] = 'success'
        return render(request, template_name,{'c':c,'expert':expert,'result':result})

@login_required
@transaction.atomic
def delete_comment_confirm(request, eid, cmtid):
    #print("=============views_update.delete_comment_confirm======")
    result = {}
    try:
        #print("==============Try========")
        expert = ExpertInfo.objects.get(eid=eid)
        c = ExpertComments.objects.get(cmtid=cmtid)
        print(expert,c)
    except:
        #print("==============ERROR========")
        result['status'] = 'error'
    else:
        c.delete()
        result['status'] = 'success'
        print(request.get_host())
        url = 'http://127.0.0.1:8000/{eid}/{ename}/commentdetail'.format(eid=eid,ename=expert.ename)
        #url = 'http://47.94.224.242:1973/{eid}/{ename}/commentdetail'.format(eid=eid,ename=expert.ename)
        return HttpResponseRedirect(url)


def delete_workexp(request, eid, expid):
    print("=============views_update.delete_workexp======")
    template_name = 'experts/workexp_detail.html'
    result = {}
    try:
        #print("==============Try========")
        expert = ExpertInfo.objects.get(eid=eid)
        exp = WorkExp.objects.get(expid=expid)
        print(expert,exp)
    except:
        #print("==============ERROR========")
        result['status'] = 'error'
    else:
        result['status'] = 'success'
        return render(request, template_name,{'exp':exp,'expert':expert,'result':result})

@transaction.atomic
def delete_workexp_confirm(request, eid, expid):
    print("=============views_update.delete_workexp_confirm======")
    result = {}
    try:
        #print("==============Try========")
        expert = ExpertInfo.objects.get(eid=eid)
        exp = WorkExp.objects.get(expid=expid)
        print(expert,exp)
    except:
        #print("==============ERROR========")
        result['status'] = 'error'
    else:
        exp.delete()
        result['status'] = 'success'
        url = 'http://127.0.0.1:8000/eid}/{ename}/workexpdetail'.format(eid=eid,ename=expert.ename)
        #url = 'http://47.94.224.242:1973/eid}/{ename}/workexpdetail'.format(eid=eid,ename=expert.ename)
        return HttpResponseRedirect(url)

