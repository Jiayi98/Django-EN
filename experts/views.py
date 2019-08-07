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
from clients.models import Client
from time import time



# Create your views here.
def base(request):
    return render(request, 'experts/home.html')

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
        return render(request, 'experts/addexpert.html', {'form': form, 'error': error})
        #print("!!!!!!!!!!!GET!!!!!!!!")
    return render(request, 'experts/addexpert.html', {'form': form, 'error':error})


@login_required
def add_comment(request,eid,ename):
    #print("!!!!!!!!!!!!!!!!!!!", ename, emobile)
    formC = CommentForm(data=request.POST)
    eproblem = request.POST.get("eproblem")
    ecomment = request.POST.get("ecomment")
    result = {}

    try:
        expert = ExpertInfo.objects.get(eid=eid)
        #myurl = 'http://47.94.224.242:1973/{eid}/{ename}/commentdetail'.format(eid=expert.eid, ename=expert.ename)
        myurl = '/{eid}/{ename}/commentdetail'.format(eid=expert.eid, ename=expert.ename)
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
            # 跳转到所有comment页面
            myurl = '/{eid}/{ename}/commentdetail'.format(eid=expert.eid, ename=expert.ename)
            #myurl = 'http://47.94.224.242:1973/{eid}/{ename}/commentdetail'.format(eid=expert.eid, ename=expert.ename)
            # 跳转到所有专家个人主页页面
            #myurl = "/{ename}/{eid}/".format(ename=ename, eid=eid)
            # myurl = "http://47.94.224.242:1973/{ename}/{eid}/".format(ename=ename, eid=eid)
            result['status'] = 'success'
            return HttpResponseRedirect(myurl)
    return render(request, 'experts/addcomment_confirm.html', {"expert":expert,"formC":formC,'result':result, 'myurl':myurl})





@login_required
def add_workexp(request,eid,ename):
    #print("===================views.py-add_workexp=========", ename, emobile)
    formW = WorkexpForm(data=request.POST)

    stime = request.POST.get("stime")
    etime = request.POST.get("etime")
    company = request.POST.get("company")
    agency = request.POST.get("agency")
    position = request.POST.get("position")
    duty = request.POST.get("duty")
    area = request.POST.get("area")
    try:
        expert = ExpertInfo.objects.get(eid=eid)
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
            newExp.save()
            # 跳转到所有工作经历页面
            myurl = '/{eid}/{ename}/workexpdetail'.format(eid=expert.eid, ename=expert.ename)
            #myurl = 'http://127.0.0.1:8000/{eid}/{ename}/workexpdetail'.format(eid=expert.eid, ename=expert.ename)
            # 跳转到所有专家个人主页页面
            #myurl = "/{ename}/{eid}/".format(ename=ename, eid=eid)
            #myurl = "http://47.94.224.242:1973/{ename}/{eid}/".format(ename=ename, eid=eid)
            return HttpResponseRedirect(myurl)
    return render(request, 'experts/addworkexp_confirm.html', {"formW":formW})




# 添加专家成功后的跳转页面
@login_required
def addok(request):
    return render(request, 'experts/add_complete.html')


def expertInfo_list(request):
    experts_list = ExpertInfo.objects.raw('select * from expert_info order by eid desc limit 100;')
    #experts_list = ExpertInfo.objects.all()[:300]
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
    expert = get_object_or_404(ExpertInfo, eid=eid)
    pay = Payment.objects.filter(eid=expert)
    p2es = Project2Expert.objects.filter(eid=expert)    # 该专家的所有访谈
    projects = set()    # 该专家所参与的所有项目
    for p2e in p2es:
        if p2e.pid not in projects:
            projects.add(p2e.pid)

    if pay.exists() == 0:
        # 没有支付方式
        pay = Payment.objects.create(eid=expert)
    else:
        pay = pay.first()

    workexps = WorkExp.objects.filter(eid=eid)
    comments = ExpertComments.objects.filter(eid=eid)
    # 7.15添加修改了添加时间显示格式
    addtime = ' {year}年{mon}月{day}日'.format(year=expert.addtime.year,mon=expert.addtime.month, day=expert.addtime.day)
    return render(request, 'experts/expert_detail.html', {'projects':projects,'addtime':addtime,'expert': expert, 'workexps':workexps,'comments': comments,'pay':pay,'p2es':p2es})





def expert_detail_update(request, ename, eid):
    error = ""
    template_name = 'experts/expert_detail_update.html'
    object = get_object_or_404(ExpertInfo, eid=eid)

    if request.method == 'POST':
        form = ExpertInfoFormUpdateDB(instance=object, data=request.POST)
        if form.is_valid():
            form.save()
            myurl = "/{ename}/{eid}/".format(ename=ename,eid=eid)
            #myurl = "http://47.94.224.242:1973/{ename}/{eid}/".format(ename=ename, eid=eid)
            return HttpResponseRedirect(myurl)
        else:
            error = "error"
            print("=======expert_detail_update/ form is invalid=========")
    else:
        form = ExpertInfoFormUpdateDB(instance=object)

    return render(request, template_name, {'expert':object,'form': form,'error':error})


def expert_contact_info_update(request, ename, eid):
    #print('==================views.expert_contact_info_update===============')
    template_name = 'experts/update_expert_contact_info.html'
    object = get_object_or_404(ExpertInfo, eid=eid)

    if request.method == 'POST':
        form = ContactInfoFormUpdateDB(instance=object, data=request.POST)
        if form.is_valid():
            form.save()
            myurl = "/{ename}/{eid}/".format(ename=ename, eid=eid)
            #myurl = "http://47.94.224.242:1973/{ename}/{eid}/".format(ename=ename, eid=eid)
            return HttpResponseRedirect(myurl)
    else:
        form = ContactInfoFormUpdateDB(instance=object)


    return render(request, template_name, {'expert': object, 'form': form, })

def comment_detail(request, eid, ename):
    #print("=================在views.py中comment_detail()==========")
    expert = get_object_or_404(ExpertInfo,eid=eid)
    comments = ExpertComments.objects.filter(eid=eid)
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
            # 跳转到该专家所有comments页面
            myurl = '/{eid}/{ename}/commentdetail'.format(eid=eid, ename=expert.ename)
            #myurl = 'http://47.94.224.242:1973/{eid}/{ename}/commentdetail'.format(eid=eid,ename=expert.ename)
            # 跳转到专家个人页面
            #myurl = "/{ename}/{eid}/".format(ename=expert.ename, eid=eid)
            #myurl = "http://47.94.224.242:1973/{ename}/{eid}/".format(ename=expert.ename, eid=eid)
            return HttpResponseRedirect(myurl)
    else:
        form = CommentFormUpdateDB(instance=comment)

    return render(request, template_name, {'comment':comment,'expert': expert,'form': form,'result':result})


def workexp_detail(request, eid, ename):
    #print("-------views.py/In Workexp_Detail-----")
    expert = get_object_or_404(ExpertInfo,eid=eid)
    workexps = WorkExp.objects.filter(eid=eid)
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
            result['status'] = 'success'
            # 跳转到所有工作经历页面
            myurl = '/{eid}/{ename}/workexpdetail'.format(eid=expert.eid, ename=expert.ename)
            #myurl = 'http://127.0.0.1:8000/{eid}/{ename}/workexpdetail'.format(eid=expert.eid, ename=expert.ename)
            # 跳转到所有专家个人主页页面
            #myurl = "http://127.0.0.1:8000/{ename}/{eid}/".format(ename=expert.ename, eid=eid)
            #myurl = "http://47.94.224.242:1973/{ename}/{eid}/".format(ename=expert.ename, eid=eid)
            return HttpResponseRedirect(myurl)
        else:
            print("=============views.py中workexp_detail_update()============")
            print("表单无效")

    else:
        form = WorkexpFormUpdateDB(instance=exp)

    return render(request, template_name, {'workexp':exp,'expert': expert,'form': form,'result':result})

def advanced_expert_form(request):
    return render(request, 'experts/advanced_expert_search.html')

def advanced_expert_search(request):
    # 对某字段进行限定 = 用户对该字段进行搜索
    template_name = 'experts/advanced_expert_search_result.html'
    eid = request.GET.get('eid')
    name = request.GET.get('name')

    trade = request.GET.get('trade')
    subtrade = request.GET.get('subtrade')
    background = request.GET.get('background')
    company = request.GET.get('company')

    info_variables = [eid, name, trade, subtrade, background]
    info_variables = [var for var in info_variables if var]
    #print(trade,type(trade),type(subtrade),type(background),type(company))
    work_variables = [company]
    work_variables = [var for var in work_variables if var]
    # 避免出现Nonetype
    if not name:
        name = ''
    if not trade:
        trade = ''
    if not subtrade:
        subtrade = ''
    if not background:
        background = ''
    if not company:
        company = ''

    print("高级搜索关键词：",info_variables, work_variables)
    if len(info_variables) == 0 and len(work_variables) == 0:
        # 没有任何限制，回到查找专家页面
        return advanced_expert_form(request)
        # expert_list = ExpertInfo.objects.all()
        # num_of_result = len(expert_list)
        #return render(request, template_name, {'num_of_result': num_of_result, 'expert_list': expert_list})
    elif eid:
        # 已知eid，直接获取对象
        expert_list = ExpertInfo.objects.filter(eid=eid)
        num_of_result = len(expert_list)
        return render(request, template_name, {'num_of_result': num_of_result, 'expert_list': expert_list})

    elif len(info_variables) == 0:
        # 对专家个人信息无限制，仅对工作经历筛选
        work_list = WorkExp.objects.filter(company__contains=company)
        expert_list = [work.eid for work in work_list]
        expert_list = list(set(expert_list))
        if company != '':
            # 搜索限定词中包括公司名，则以"公司限定搜索词"与专家公司名称相似度排序
            expert_list = search_sort_helper(expert_list, company)
        num_of_result = len(expert_list)
        return render(request, template_name, {'num_of_result': num_of_result, 'expert_list': expert_list})

    elif len(work_variables) == 0:
        # 对工作经历无限制，仅通过对专家信息的条件限制筛选
        keywords = background.split()   # 对背景字段的搜索词进行分隔
        if len(keywords) >= 1:
            #   背景有一个或多个搜索词
            print(keywords)
            temp = ExpertInfo.objects.filter(ename__contains=name,
                                             etrade__contains=trade,
                                             esubtrade__contains=subtrade,
                                             ebackground__contains=keywords[0]
                                             )

            print("第一次筛选结果数量：",len(temp))
            keywords = keywords[1:]     # 获取第一个之后的搜索词
            for k in keywords:
                pool = temp
                temp = []
                for expert in pool:
                    if expert.ebackground and k in expert.ebackground:
                        temp.append(expert)
                print("本次筛选关键词为：",k, "筛选结果数量：", len(temp))
                if len(temp) == 0:
                    break

            expert_list = temp
        else:
            expert_list = ExpertInfo.objects.filter(
                ename__contains=name,
                etrade__contains=trade,
                esubtrade__contains=subtrade
                )

        num_of_result = len(expert_list)
        print("num_of_result:", num_of_result)
        return render(request, template_name, {'num_of_result': num_of_result, 'expert_list': expert_list})

    else:
        # 既对工作经历有限制，又对专家信息有限制
        result_list = WorkExp.objects.filter(company__contains=company)
        expert_list = []
        keywords = background.split()
        print("先通过公司限制筛选出的结果数量：",len(result_list))    # 对背景字段的搜索词进行分隔
        for workexp in result_list:
            expert = workexp.eid
            if name in info_variables and (not expert.ename or name not in expert.ename):
                continue
            if trade in info_variables and (not expert.etrade or trade not in expert.etrade):
                continue
            if subtrade in info_variables and (not expert.esubtrade or trade not in expert.esubtrade):
                continue
            if expert not in expert_list:
                expert_list.append(expert)

        if len(keywords) >= 1:
            # 对背景有限制条件
            temp = expert_list
            print("temp:", len(temp))

            for k in keywords:
                pool = temp
                temp = []
                print("本次筛选关键词为：", k)
                for expert in pool:
                    if expert.ebackground and k in expert.ebackground:
                        temp.append(expert)
                print("本次筛选关键词为：",k, "筛选结果数量：", len(temp))
                if len(temp) == 0:
                    break

            expert_list = temp

        expert_list = search_sort_helper(expert_list, company)
        num_of_result = len(expert_list)
        return render(request, template_name, {'num_of_result': num_of_result, 'expert_list': expert_list})





def search_expert(request):
    #t = time()
    q = request.GET.get('q')
    error_msg = ''
    print("========== 全局搜索搜索关键词： ",q)
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'experts/base.html', {'error_msg': error_msg})

    expert_list = get_expert_list(q)
    num_of_result = len(expert_list)
    #print("时间：",time() - t)
    # 可对所有模块进行全局搜索
    #client_list = get_client_list(q)
    #project_list = get_project_list(q)
    #print(len(expert_list), len(client_list), len(project_list))
    return render(request, 'experts/search_expert_results.html', {'num_of_result':num_of_result,'q':q,'error_msg': error_msg,'expert_list': expert_list,})


def get_client_list(q):
    client_list = []
    result_list1 = Client.objects.filter( Q(cname__contains=q) |
                                        Q(bc_name__contains=q) |
                                        Q(fc_name__contains=q) |
                                        Q(cpolicy__contains=q) |
                                        Q(ctype__contains=q) |
                                        Q(cinfo__contains=q) |
                                        Q(cremark__contains=q)
                                        )
    client_list = list(set(result_list1))
    return client_list

def get_project_list(q):
    project_list = []
    result_list1 = Project.objects.filter(Q(pname__contains=q) |
                                            Q(cname__contains=q) |
                                            Q(pm__contains=q) |
                                            Q(pm_mobile__contains=q) |
                                            Q(pm_wechat__contains=q) |
                                            Q(pm_email__contains=q) |
                                            Q(premark__contains=q) |
                                            Q(pdetail__contains=q)
                                          )
    project_list = list(set(result_list1))
    return project_list

def get_expert_list(q):
    expert_list = []
    result_list1 = []
    result_list2 = []
    result_list3 = []

    if isContainChinese(q):
        result_list1 = ExpertInfo.objects.filter(
            Q(ename__contains=q) |
            Q(emobile__contains=q) |
            Q(eemail__contains=q) |
            Q(etrade__contains=q) |
            Q(esubtrade__contains=q) |

            Q(elocation__contains=q) |
            Q(ecomefrom__contains=q) |
            Q(eremark__contains=q) |
            Q(ebackground__contains=q)
        )

        result_list2 = ExpertComments.objects.filter(
            Q(eproblem__contains=q) | Q(ecomment__contains=q))
        temp2 = [comment.eid for comment in result_list2]

        result_list3 = WorkExp.objects.filter(
            Q(company__contains=q) |
            Q(agency__contains=q) |
            Q(position__contains=q) |
            Q(duty__contains=q)
        )
        temp3 = [workexp.eid for workexp in result_list3]

    else:

        result_list1 = ExpertInfo.objects.filter(Q(ename__icontains=q) |
                                                 Q(emobile__icontains=q) |
                                                 Q(eemail__icontains=q) |
                                                 Q(etrade__icontains=q) |
                                                 Q(esubtrade__icontains=q) |

                                                 Q(elocation__icontains=q) |
                                                 Q(ecomefrom__icontains=q) |
                                                 Q(eremark__icontains=q) |
                                                 Q(ebackground__icontains=q)
                                                 )

        result_list2 = ExpertComments.objects.filter(Q(eproblem__icontains=q) | Q(ecomment__icontains=q))
        temp2 = [comment.eid for comment in result_list2]

        result_list3 = WorkExp.objects.filter(
            Q(company__icontains=q) |
            Q(agency__icontains=q) |
            Q(position__icontains=q) |
            Q(duty__icontains=q)
        )
        temp3 = [workexp.eid for workexp in result_list3]

    items = chain(result_list1, temp2, temp3)    # 合并三个lists
    expert_list = list(set(items))    # 去重后变回list，因为不可对set进行排序
    expert_list = search_sort_helper(expert_list, q)
    return expert_list

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
            #myurl = "/{ename}/{eid}/".format(ename=pay.eid.ename,eid=pay.eid.eid)
            myurl = "/{ename}/{eid}/".format(ename=pay.eid.ename,eid=pay.eid.eid)
            print(myurl)
            return HttpResponseRedirect(myurl)
        else:
            print("=============views.get_payment_update()============")
            print("表单无效")
    else:
        form = PaymentForm(instance=pay)

    return render(request, template_name, {'expert': pay.eid, 'pay': pay, 'form': form,})
