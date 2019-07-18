from django.shortcuts import render
from django.db.models import Q
from itertools import chain
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import ExpertInfo,ExpertComments,WorkExp,Payment
from .forms import ExpertInfoForm, CommentForm,WorkexpForm,deleteConfirmForm,PaymentForm

from .forms_update import ExpertInfoFormUpdateDB,CommentFormUpdateDB, WorkexpFormUpdateDB,ExpertInfoFormUpdate,ContactInfoFormUpdateDB

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required
from projects.models import Project,Project2Expert
"""
def export_all_excel(request):
    print("==========views.export_all_excel========")
    exp = ExpertInfo()
    alert_text = exp.export_excel(None)
    return HttpResponse(alert_text)
"""

# Create your views here.
def base(request):
    return render(request, 'experts/base.html')

@login_required
def expert_contact_info(request, ename, eid):
    template_name = 'experts/expert_contact_info.html'
    expert = get_object_or_404(ExpertInfo, eid=eid)
    msg = 'success'
    if request.user.has_perm('查看联系方式'):
        #print("有权限")
        #print("=============views.expert_contact_info======")
        #template_name = 'experts/expert_contact_info.html'
        #expert = get_object_or_404(ExpertInfo, eid=eid)
        msg = 'success'
    else:
        #print("无权限")
        #template_name = 'experts/no_permission.html'
        msg = "error"
    return render(request, template_name, {'expert': expert,'msg':msg})


@login_required
def myDelete(request, eid, ename):
    #print("=============views.DELETE======")
    template_name = 'experts/delete.html'
    expert = get_object_or_404(ExpertInfo, ename=ename, eid=eid)
    return render(request, 'experts/delete.html', {'expert':expert})

#def deleteConfirm(request):
def delete_confirm(request, eid,ename):
    #print("=============views.delete_confirm======")
    template_name = 'experts/delete_confirm.html'
    result = {}
    form = deleteConfirmForm(request.POST)
    name = request.POST.get('ename')
    eid = request.POST.get('eid')
    if request.method == 'POST' and request.POST:
        #print("==============进来了=")
        if form.is_valid():
            try:
                #print("==============Try========")
                expert = ExpertInfo.objects.get(ename=ename,eid=eid)
                #print(expert)
            except:
                #print("==============ERROR========")
                result['status'] = 'error'
            else:
                expert.delete()
                result['status'] = 'success'
                return HttpResponseRedirect('/addcomplete/')

        else:
            print("=============views.delete_confirm======")
            print("==============form is INVALID========")
    else:
        form = deleteConfirmForm(request.POST)

    return render(request, template_name, {'form':form,'result':result})

"""
EXPERTS INFORMATION
"""

"""
@login_required
def addExpert(request):
    form = ExpertInfoForm()
    return render(request, 'experts/addexpert.html', {'form': form})
"""

@login_required
def addExpert(request):
    form = ExpertInfoForm()
    error = ""
    if request.method == "POST":
        expertInfo_form = ExpertInfoForm(data=request.POST)
        if expertInfo_form.is_valid():
            new_expert = expertInfo_form.save(commit=False)
            # filter得到的是一个list，而不是一个object
            expert = ExpertInfo.objects.filter(ename=new_expert.ename, emobile=new_expert.emobile, eemail=new_expert.eemail)
            if expert.exists() == 0:
                new_expert = expertInfo_form.save()
                return HttpResponseRedirect('/addcomplete/')
            else:
                print("!!!!!!!!!!!This expert already existed!!!!!!!!")
                error = "error"
                return render(request, 'experts/addexpert.html', {'form': form, 'error': error})
        else:
            print("=============views.addExpertToDatabase======")
            print("-----------NOT VALID----------")
            error = "error"
    else:
        print("!!!!!!!!!!!GET!!!!!!!!")

    # 重定向
    #return HttpResponseRedirect('/addcomplete/')
    return render(request, 'experts/addexpert.html', {'form': form, 'error':error})

"""
"""


@login_required
def addComment(request):
    formI = ExpertInfoFormUpdate()
    ename = request.POST.get("ename")
    expert_objs = ExpertInfo.objects.filter(ename=ename)

    return render(request, 'experts/addcomment.html', {'formI': formI, 'expert_objs': expert_objs})
    #return render(request, 'experts/addcomment.html', {'formC': formC,'formI':formI,'expert_objs':expert_objs})



@login_required
def add_comment(request,ename,emobile):
    #print("!!!!!!!!!!!!!!!!!!!", ename, emobile)
    formC = CommentForm(data=request.POST)
    eproblem = request.POST.get("eproblem")
    ecomment = request.POST.get("ecomment")
    result = {}

    try:
        expert = ExpertInfo.objects.get(ename=ename, emobile=emobile)
        #47.94.224.242:1973
        #myurl = 'http://47.94.224.242:1973/{eid}/{ename}/commentdetail'.format(eid=expert.eid, ename=expert.ename)
        myurl = 'http://127.0.0.1:8000/{eid}/{ename}/commentdetail'.format(eid=expert.eid, ename=expert.ename)
    except:
        print("=============views.add_comment======")
        print("!!!!!!!!!!!This expert not exist!!!!!!!!")
        return HttpResponseRedirect('/addecomment/')
    else:
        #print("----------Expert Exists----------")

        if request.method == "POST":
            #print("----------进来了----------")
            newComment = ExpertComments()
            newComment.eid_id = expert.eid
            newComment.eproblem = eproblem
            newComment.ecomment = ecomment
            newComment.save()
            # 47.94.224.242:1973
            myurl = 'http://127.0.0.1:8000/{eid}/{ename}/commentdetail'.format(eid=expert.eid, ename=expert.ename)
            #myurl = 'http://47.94.224.242:1973/{eid}/{ename}/commentdetail'.format(eid=expert.eid, ename=expert.ename)
            result['status'] = 'success'
            return HttpResponseRedirect(myurl)
    return render(request, 'experts/addcomment_confirm.html', {"expert":expert,"formC":formC,'result':result, 'myurl':myurl})




@login_required
def addWorkexp(request):
    #formW = WorkexpForm()
    formI = ExpertInfoFormUpdate()

    ename = request.POST.get("ename")
    expert_objs = ExpertInfo.objects.filter(ename=ename)
    #for obj in expert_objs:
    #    print(obj.eid)
    return render(request, 'experts/addworkexp.html', {'formI': formI, 'expert_objs': expert_objs})
    #return render(request, 'experts/addworkexp.html', {'formW': formW, 'formI': formI, 'expert_objs': expert_objs})




@login_required
def add_workexp(request,ename,emobile):
    #print("===================views.py-add_workexp=========", ename, emobile)
    formW = WorkexpForm(data=request.POST)

    stime = request.POST.get("stime")
    etime = request.POST.get("etime")
    company = request.POST.get("company")
    agency = request.POST.get("agency")
    position = request.POST.get("position")
    duty = request.POST.get("duty")
    area = request.POST.get("area")
    #istonow = request.POST.get("istonow")
    try:
        expert = ExpertInfo.objects.get(ename=ename, emobile=emobile)
        #print(expert.eid)
    except:
        print("=============views.add_workexp======")
        print("!!!!!!!!!!!This expert not exist!!!!!!!!")
        return HttpResponseRedirect('/addecomment/')
    else:
        #print("----------Expert Exists----------")

        if request.method == "POST":
            #print("----------进来了----------")
            newExp = WorkExp()
            newExp.eid_id = expert.eid
            newExp.stime = stime
            newExp.etime = etime
            newExp.company = company
            newExp.agency = agency
            newExp.position = position
            newExp.duty = duty
            newExp.area = area
            #newExp.istonow = istonow
            newExp.save()
            # 47.94.224.242:1973
            #url = 'http://47.94.224.242:1973/{eid}/{ename}/workexpdetail'.format(eid=expert.eid, ename=expert.ename)
            url = 'http://127.0.0.1:8000/{eid}/{ename}/workexpdetail'.format(eid=expert.eid, ename=expert.ename)
            return HttpResponseRedirect(url)
            #return HttpResponseRedirect('/addcomplete/')
    return render(request, 'experts/addworkexp_confirm.html', {"formW":formW})




# 返回页面addok
@login_required
def addok(request):
    return render(request, 'experts/add_complete.html')


def expertInfo_list(request):
    experts_list = ExpertInfo.objects.all()[:300]
    paginator = Paginator(experts_list, 30)
    page = request.GET.get('page')
    try:
        experts = paginator.page(page)
    except PageNotAnInteger:
        experts = paginator.page(1)
    except EmptyPage:
        experts = paginator.page(paginator.num_pages)
    return render(request, 'experts/expertinfo_list.html', {'page':page, 'experts':experts})

def expert_detail(request, ename, eid):
    # if not request.user.has_perm(''):
    #    raise PermissionDenied
    #print("===========views.expert_detail=========")
    expert = get_object_or_404(ExpertInfo, eid=eid)
    pay = Payment.objects.filter(eid=expert)
    p2es = Project2Expert.objects.filter(eid=expert)

    if pay.exists() == 0:
        # 没有支付方式
        pay = Payment.objects.create(eid=expert)
    else:
        pay = pay.first()
    print('--------------',pay)
    workexps = WorkExp.objects.filter(eid=eid)
    comments = ExpertComments.objects.filter(eid=eid)
    # 7.15添加修改了添加时间显示格式
    addtime = ' {year}年{mon}月{day}日'.format(year=expert.addtime.year,mon=expert.addtime.month, day=expert.addtime.day)
    return render(request, 'experts/expert_detail.html', {'addtime':addtime,'expert': expert, 'workexps':workexps,'comments': comments,'pay':pay,'p2es':p2es})
    #return render(request, 'experts/expert_detail.html', {'expert':expert, 'comments':comments})


def expert_detail_update(request, ename, eid):
    template_name = 'experts/expert_detail_update.html'
    object = get_object_or_404(ExpertInfo, eid=eid)
    if request.method == 'POST':
        form = ExpertInfoFormUpdateDB(instance=object, data=request.POST)
        if form.is_valid():
            form.save()
            # if is_ajax(), we just return the validated form, so the modal will close
            myurl = "http://127.0.0.1:8000/{ename}/{eid}/".format(ename=ename,eid=eid)
            #myurl = "http://47.94.224.242:1973/{ename}/{eid}/".format(ename=ename, eid=eid)
            return HttpResponseRedirect(myurl)
    else:
        form = ExpertInfoFormUpdateDB(instance=object)

    return render(request, template_name, {'expert':object,'form': form,})

# 7.15 修改联系方式
def expert_contact_info_update(request, ename, eid):
    print('==================views.expert_contact_info_update===============')
    template_name = 'experts/update_expert_contact_info.html'
    object = get_object_or_404(ExpertInfo, eid=eid)

    if request.method == 'POST':
        form = ContactInfoFormUpdateDB(instance=object, data=request.POST)
        if form.is_valid():
            form.save()
            # if is_ajax(), we just return the validated form, so the modal will close
            myurl = "http://127.0.0.1:8000/expert_contact_info/{ename}/{eid}/".format(ename=ename, eid=eid)
            #myurl = "http://47.94.224.242:1973/expert_contact_info/{ename}/{eid}/".format(ename=ename, eid=eid)
            return HttpResponseRedirect(myurl)
    else:
        form = ContactInfoFormUpdateDB(instance=object)


    return render(request, template_name, {'expert': object, 'form': form, })

def comment_detail(request, eid, ename):
    # if not request.user.has_perm(''):
    #    raise PermissionDenied
    #print("=================在views.py中comment_detail()==========")
    expert = get_object_or_404(ExpertInfo,eid=eid)
    comments = ExpertComments.objects.filter(eid=eid)
    #print(eid)
    #for c in comments:
    #    print(c.cmtid)
    return render(request, 'experts/comment_detail.html', {'expert':expert,'comments': comments})

# 刚加的
def comment_detail_update(request, eid, cmtid):
    #print("=============views.py中comment_detail_update()")
    template_name = 'experts/comment_detail_update.html'
    expert = get_object_or_404(ExpertInfo, eid=eid)
    comment = get_object_or_404(ExpertComments, cmtid=cmtid)
    result = {}
    if request.method == 'POST':
        form = CommentFormUpdateDB(instance=comment, data=request.POST)

        if form.is_valid():
            #print("=============form is valid =============", form.is_valid())
            form.save()
            result['status'] = 'success'
    else:
        form = CommentFormUpdateDB(instance=comment)

    return render(request, template_name, {'comment':comment,'expert': expert,'form': form,'result':result})


def workexp_detail(request, eid, ename):
    # if not request.user.has_perm(''):
    #    raise PermissionDenied
    #print("-------views.py/In Workexp_Detail-----")
    expert = get_object_or_404(ExpertInfo,eid=eid)
    workexps = WorkExp.objects.filter(eid=eid)
    #print(eid)
    #for w in workexps:
    #    print(w.expid)
    return render(request, 'experts/workexp_detail.html', {'expert':expert,'workexps': workexps})

# 刚加的
def workexp_detail_update(request, eid, expid):
    #print("=============views.py中workexp_detail_update()")
    template_name = 'experts/workexp_detail_update.html'
    expert = get_object_or_404(ExpertInfo, eid=eid)
    exp = get_object_or_404(WorkExp, expid=expid)
    result = {}
    if request.method == 'POST':
        form = WorkexpFormUpdateDB(instance=exp, data=request.POST)
        if form.is_valid():
            form.save()
            # if is_ajax(), we just return the validated form, so the modal will close
            #print("成功")
            result['status'] = 'success'
        else:
            print("=============views.py中workexp_detail_update()============")
            print("表单无效")
        #return HttpResponseRedirect('/addcomplete/')
    else:
        form = WorkexpFormUpdateDB(instance=exp)

    return render(request, template_name, {'workexp':exp,'expert': expert,'form': form,'result':result})

def advanced_expert_form(request):
    trade_list = ExpertInfo.objects.values("etrade").distinct()
    trade_list = set([item[key] for item in trade_list for key in item])
    #print(len(trade_list))
    subtrade_list = ExpertInfo.objects.values("esubtrade").distinct()
    subtrade_list = set([item[key] for item in subtrade_list for key in item])
    #print(len(subtrade_list))
    locations = ExpertInfo.objects.values("elocation").distinct()
    locations = set([item[key] for item in locations for key in item])
    #print(len(locations))
    return render(request, 'experts/advanced_expert_search.html',{'trade_list':trade_list,'subtrade_list':subtrade_list,'locations':locations})

def advanced_expert_search(request):
    template_name = 'experts/advanced_expert_search_result.html'
    eid = request.GET.get('eid')
    name = request.GET.get('name')
    sex =request.GET.get('sex')
    location =request.GET.get('location')
    trade = request.GET.get('trade')
    subtrade = request.GET.get('subtrade')
    background = request.GET.get('background')
    company = request.GET.get('company')
    agency = request.GET.get('agency')
    position = request.GET.get('position')
    duty = request.GET.get('duty')
    area = request.GET.get('area')

    info_variables = [eid,name,sex,location,trade,subtrade,background]
    info_variables = [var for var in info_variables if var]
    work_variables = [company,agency,position,duty,area]
    work_variables = [var for var in work_variables if var]

    # DEBUG

    #for q in info_variables:
    #    print("========== 搜索关键词： ", q)
    #for q in work_variables:
    #    print("========== 搜索关键词： ", q)

    if len(info_variables) == 0 and len(work_variables) == 0:
        # 没有任何限制，直接获取所有专家
        expert_list = ExpertInfo.objects.all()
        return render(request, template_name, {'expert_list': expert_list})
    elif eid:
        expert_list = ExpertInfo.objects.filter(eid=eid)
        return render(request, template_name, {'expert_list': expert_list})
    elif len(work_variables) == 0:
        # 对工作经历无限制，通过对专家信息的条件限制筛选
        #print("对工作经历无限制，通过对专家信息的条件限制筛选")
        expert_list = ExpertInfo.objects.filter(
            ename__contains=name,
            esex__icontains=sex,
            etrade__contains=trade,
            esubtrade__contains=subtrade,
            elocation__contains=location,
            ebackground__contains=background
        )
        #DEBUG
        return render(request, template_name, {'expert_list': expert_list})
    elif len(info_variables) == 0:
        # 对专家个人信息无限制，通过对工作经历的条件限制筛选
        #print("对专家个人信息无限制，通过对工作经历的条件限制筛选")
        work_list = WorkExp.objects.filter(
            company__contains=company,
            agency__contains=agency,
            position__contains=position,
            duty__contains=duty,
            area__contains=area
        )
        # DEBUG
        expert_list = [work.eid for work in work_list]
        #print(len(expert_list))
        if company != '':
            #print("排序！！")
            expert_list = search_sort_helper(expert_list, company)
        return render(request, template_name, {'expert_list': expert_list})
    else:
        # 对专家个人信息、工作经历都有条件限制，取交集进行筛选

        if len(info_variables) < len(work_variables):
            # 对工作经历的条件更多
            result_list = WorkExp.objects.filter(
                company__contains=company,
                agency__contains=agency,
                position__contains=position,
                duty__contains=duty,
                area__contains=area
            )
            expert_list = []
            for work in result_list:
                exp = work.eid
                if name in info_variables and name not in exp.ename:
                    continue
                if sex in info_variables and (not exp.esex or sex != exp.esex):
                    continue
                if location in info_variables and (not exp.elocation or location not in exp.elocation):
                    continue
                if trade in info_variables and (not exp.etrade or trade not in exp.etrade):
                    continue
                if subtrade in info_variables and (not exp.esubtrade or subtrade not in exp.esubtrade):
                    continue
                if background in info_variables and (not exp.ebackground or background not in exp.ebackground):
                    continue
                expert_list.append(exp)
            # DEBUG
            # print(len(expert_list))
            return render(request, template_name, {'expert_list': expert_list})

        else:
            result_list = ExpertInfo.objects.filter(
                ename__contains=name,
                esex__icontains=sex,
                etrade__contains=trade,
                esubtrade__contains=subtrade,
                elocation__contains=location,
                ebackground__contains=background
            )
            expert_list = []
            for exp in result_list:
                workexp = WorkExp.objects.filter(eid=exp.eid)
                stored = False
                for work in workexp:
                    if company in work_variables and (not work.company or company not in work.company):
                        continue
                    if agency in work_variables and (not work.agency or agency not in work.agency):
                        continue
                    if position in work_variables and (not work.position or position not in work.position):
                        continue
                    if duty in work_variables and (not work.duty or duty not in work.duty):
                        continue
                    if area in work_variables and (not work.area or area not in work.area):
                        continue
                    if not stored:
                        stored = True
                        expert_list.append(exp)
            # DEBUG
            # workexp_list = [WorkExp.objects.filter(eid=expert.eid) for expert in expert_list]
            # print(len(expert_list))
            if company != '':
                #print("排序！！")
                expert_list = search_sort_helper(expert_list, company)
            return render(request, template_name, {'expert_list': expert_list})

def search_expert(request):
    q = request.GET.get('q')
    error_msg = ''
    print("========== 搜索关键词： ",q)
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'experts/base.html', {'error_msg': error_msg})
    expert_list = []
    result_list1 =[]
    result_list2 = []
    result_list3 = []
    if isContainChinese(q):
        result_list1 = ExpertInfo.objects.filter(
                                            Q(ename__contains=q) |
                                            Q(esex__contains=q)|
                                            Q(emobile__contains=q) |
                                            Q(eemail__contains=q)|
                                            Q(etrade__contains=q) |
                                            Q(esubtrade__contains=q)|


                                            Q(elocation__contains=q) |
                                            Q(estate__contains=q) |
                                            Q(ecomefrom__contains=q) |
                                            Q(eremark__contains=q) |
                                            Q(addtime__contains=q)|
                                            Q(ebackground__contains=q)
                                         )


        result_list2 = ExpertComments.objects.filter(
                                                 Q(eproblem__contains=q) | Q(ecomment__contains=q))

        result_list3 = WorkExp.objects.filter(
                                          Q(company__contains=q) |
                                          Q(agency__contains=q) |
                                          Q(position__contains=q) |
                                          Q(duty__contains=q) |
                                          Q(area__contains=q)
                                          )

    else:

        result_list1 = ExpertInfo.objects.filter(Q(ename__icontains=q) |
                                                Q(esex__icontains=q)|
                                                Q(emobile__icontains=q) |
                                                Q(eemail__icontains=q)|
                                                Q(etrade__icontains=q) |
                                                Q(esubtrade__icontains=q)|


                                                Q(elocation__icontains=q) |
                                                Q(estate__icontains=q) |
                                                Q(ecomefrom__icontains=q) |
                                                Q(eremark__icontains=q) |
                                                Q(ebackground__icontains=q) |
                                                Q(addtime__icontains=q)
                                                )

        result_list2 = ExpertComments.objects.filter(Q(eproblem__icontains=q) | Q(ecomment__icontains=q))

        result_list3 = WorkExp.objects.filter(
                                              Q(company__icontains=q) |
                                              Q(agency__icontains=q) |
                                              Q(position__icontains=q) |
                                              Q(duty__icontains=q) |
                                              Q(area__icontains=q)
                                            )

    items = chain(result_list1, result_list2, result_list3)
    #items = chain(result_list1, result_list2)
    for item in items:
        if type(item) is ExpertInfo:
            expert_list.append(item)
            #print(item, "========expert")
        elif type(item) is ExpertComments:
            try:
                expert = item.eid
            except:
                pass
            else:
                expert_list.append(expert)
            #print(expert, "=======comments")
        else:
            try:
                expert = item.eid
            except:
                pass
            else:
                expert_list.append(expert)
            #print(expert,"=====workexp")
    expert_list = list(set(expert_list))

    expert_list = search_sort_helper(expert_list, q)
    return render(request, 'experts/search_expert_results.html', {'error_msg': error_msg,'expert_list': expert_list})

def search_sort_helper(expert_list, q):
    new_list = []
    for exp in expert_list:
        index = get_index(exp, q)
        obj = [exp, index]
        new_list.append(obj)

    new_list = sorted(new_list, reverse=True, key=comparator)
    # print(new_list)
    expert_list = [elem[0] for elem in new_list]
    return expert_list

def get_index(exp,q):
    company_name = exp.get_company()
    company_len = len(company_name)
    str_count = len(company_name.split(q)) - 1
    #print(str_count)
    if(company_len == 0):
        return 0
    else:
        index = str_count/company_len
        return index

def comparator(elem):
    return elem[1]

def isContainChinese(s):
    for c in s:
        if ('\u4e00' <= c <= '\u9fa5'):
            return True
    return False

def get_payment_update(request, ep_id):
    template_name = 'experts/payment_update.html'
    print("========experts/views.get_payment_update========")
    print(ep_id)
    pay = get_object_or_404(Payment, ep_id=ep_id)

    if request.method == 'POST':
        form = PaymentForm(instance=pay, data=request.POST)
        if form.is_valid():
            form.save()
            #myurl = "http://47.94.224.242:1973/{ename}/{eid}/".format(ename=pay.eid.ename,eid=pay.eid.eid)
            myurl = "http://127.0.0.1:8000/{ename}/{eid}/".format(ename=pay.eid.ename,eid=pay.eid.eid)
            print(myurl)
            return HttpResponseRedirect(myurl)
        else:
            print("=============views.py中workexp_detail_update()============")
            print("表单无效")
        # return HttpResponseRedirect('/addcomplete/')
    else:
        form = PaymentForm(instance=pay)

    return render(request, template_name, {'expert': pay.eid, 'pay': pay, 'form': form,})
