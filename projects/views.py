from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from experts.models import ExpertInfo,WorkExp
from clients.models import Client,BusinessContact
from projects.models import Project
from .forms import *
import django.utils.timezone as timezone
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@login_required
def delete_project(request, pid):
    template_name = 'projects/project_detail.html'
    project = get_object_or_404(Project,pid=pid)
    result = project.delete()
    if result:
        return HttpResponseRedirect('/project_info_list/')
    else:
        result = '删除失败'
    return render(request, template_name,{'result':result})

@login_required
def delete_p2e(request, pteid, pid):
    template_name = 'projects/project_detail.html'
    p2e = get_object_or_404(Project2Expert, pteid=pteid)
    project = get_object_or_404(Project,pid=pid)

    # 删除一次访谈记录，对应专家的访谈次数字段更新
    expert = p2e.eid
    expert.interview_num = expert.interview_num - 1
    expert.save()

    result = p2e.delete()
    if result:
        myurl = '/project_detail/{pid}/{cid}/'.format(pid=pid, cid=project.cid.cid)
        #myurl = 'http://47.94.224.242:1973/project_detail/{pid}/{cid}/'.format(pid=pid, cid=project.cid.cid)
        return HttpResponseRedirect(myurl)
    else:
        result = '删除失败'
    return render(request, template_name,{'result':result})

@login_required
def project(request):
    return render(request, 'projects/project_base.html')

@login_required
def project_info_list(request):
    projects_list = Project.objects.all()[:100]
    paginator = Paginator(projects_list, 20)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'projects/project_info_list.html', {'page':page, 'projects':projects})

@login_required
def interview_info_list(request):
    interview_list = Project2Expert.objects.all()
    paginator = Paginator(interview_list, 20)
    page = request.GET.get('page')
    try:
        interviews = paginator.page(page)
    except PageNotAnInteger:
        interviews = paginator.page(1)
    except EmptyPage:
        interviews = paginator.page(paginator.num_pages)
    return render(request, 'projects/interview_info_list.html', {'page':page, 'interviews':interviews})

@login_required
def client_interview_info_list(request):
    interview_list = Project2Expert.objects.all()
    paginator = Paginator(interview_list, 20)
    page = request.GET.get('page')
    try:
        interviews = paginator.page(page)
    except PageNotAnInteger:
        interviews = paginator.page(1)
    except EmptyPage:
        interviews = paginator.page(paginator.num_pages)
    return render(request, 'projects/client_interview_info_list.html', {'page':page, 'interviews':interviews})

@login_required
def project_detail(request, pid, cid):
    project = get_object_or_404(Project, pid=pid)
    client = Client.objects.filter(cid=cid).first()
    experts = get_object_or_404(Project, pid=pid).expertinfos.all().distinct()

    p2es = Project2Expert.objects.filter(pid=pid)

    return render(request, 'projects/project_detail.html', {'experts':experts,'project': project, 'client': client, 'p2es': p2es,'createtime':project.pcreatetime})

# 添加项目访谈
@login_required
def add_p2e(request,pid):
    form = P2EForm(data=request.POST)
    project = Project.objects.get(pid=pid)
    ename = request.POST.get('ename')
    eid_num = request.POST.get("eid")
    flag = {}
    if request.method == "POST":
        try:
            expert = ExpertInfo.objects.get(eid=eid_num)
        except:
            flag['status'] = 'error'
        else:
            if not ename or expert.ename == ename:
                # 添加一次访谈时同时更新专家信息表中访谈次数字段
                if not expert.interview_num:
                    expert.interview_num = 1
                    expert.save()
                else:
                    expert.interview_num = expert.interview_num + 1
                    expert.save()
                year = timezone.now().year
                month = timezone.now().month
                if month < 10:
                    month = '0{m}'.format(m=month)
                day = timezone.now().day
                if day < 10:
                    day = '0{d}'.format(d=day)
                date = "{y}-{m}-{d}".format(y=year,m=month,d=day)
                new_obj = Project2Expert.objects.create(eid=expert,pid=project,c_payment=0.0,e_payment=0.0, interviewer=request.user.username,itv_date=date,itv_stime='00:00',itv_etime='24:00',avg_score=0.0)
                myurl = '/projects/update_p2e_detail/{pteid}/'.format(pteid=new_obj.pteid)
                return HttpResponseRedirect(myurl)
            else:
                flag['status'] = 'error'
    return render(request, 'projects/add_p2e.html', {"project": project, "form": form,'flag':flag})

# 修改项目访谈信息
def update_p2e_detail(request,pteid):
    object = get_object_or_404(Project2Expert, pteid=pteid)
    #print(type(object.pid),type(object.eid))
    origin_itv_paid_duration = object.itv_paid_duration
    origin_itv_duration = object.itv_duration
    origin_status = object.status
    result = {}
    if request.method == 'POST':
        form = Project2ExpertForm(instance=object, data=request.POST)
        if form.is_valid():
            form.save()
            if object.itv_paid_duration != origin_itv_paid_duration and object.status == 1:
                #如果计费时长发生改变则更新专家付费和客户收费总价 且 访谈状态为已访谈
                client = object.pid.cid
                object.c_payment = (client.cfee* 0.25) * object.fee_index * (object.itv_paid_duration//15)    #用计费市场计算客户收费
                object.save()

            if object.itv_duration != origin_itv_duration and object.status == 1:
                expert = object.eid
                if object.itv_duration % 15 > 5:
                    # 访谈时长超过5分钟向上取整
                    object.e_payment = (expert.efee * 0.25) * (object.itv_duration // 15 + 1)  # 用访谈时长计算专家付费
                else:
                    object.e_payment = (expert.efee * 0.25) * (object.itv_duration//15)    #用访谈时长计算专家付费
                object.save()
            #if origin_status == 1 and object.status == 0:
            #    # 如果访谈状态从1变为0，则三项访谈评分重置为0
            #    object.knowledge = 0
            #    object.communication = 0
            #    object.cooperation = 0
            #    object.avg_score = 0.0

            object.avg_score = round((object.knowledge + object.communication + object.cooperation) / 3.0,2)
            object.save()
            result['status'] = 'success'
            myurl = '/project_detail/{pid}/{cid}/'.format(pid=object.pid.pid, cid=object.pid.cid.cid)
            #myurl = 'http://47.94.224.242:1973/project_detail/{pid}/{cid}/'.format(pid=object.pid.pid, cid=object.pid.cid.cid)
            return HttpResponseRedirect(myurl)
        else:
            username = 'unknown'
            if request.user.is_authenticated():
                username = request.user.username
            print("projects/views.update_p2e_detail")
            print(username, "FORM NOT VALID")
    else:
        form = Project2ExpertForm(instance=object)

    return render(request, 'projects/update_p2e_detail.html', {'object': object,'project':object.pid,'expert':object.eid,'form': form, 'result': result, })

@login_required
def add_project(request):
    form = ProjectForm()
    return render(request, 'projects/add_project.html', {'form': form})


@login_required
def addProjectToDatabase(request):
    if request.method == "POST":
        pname = request.POST.get('pname')
        pm = request.POST.get('pm')
        pdeadline = request.POST.get('pdeadline')
        pcreatetime = request.POST.get('pcreatetime')
        premark = request.POST.get('premark')
        person_in_charge = request.POST.get('person_in_charge')
        pdetail = request.POST.get('pdetail')
        cid_num = request.POST.get('cid')
        try:
            client = Client.objects.get(cid=cid_num)
        except:
            return HttpResponseRedirect('/project_info_list/')
        else:
            # filter得到的是一个list，而不是一个object
            project = Project.objects.filter(pname=pname, cid=client)
            if project.exists() == 0:
                cid = client
                new_project = Project()
                new_project.cid = cid
                new_project.pname = pname
                new_project.pm = pm
                new_project.pdeadline = pdeadline
                new_project.pcreatetime = pcreatetime
                new_project.premark = premark
                new_project.pdetail = pdetail
                new_project.person_in_charge = person_in_charge
                new_project.save()

            else:
                print("!!!!!!!!!!!This project already existed!!!!!!!!")

    else:
        print("!!!!!!!!!!!GET!!!!!!!!")

    # 重定向
    return HttpResponseRedirect('/project_info_list/')

@login_required
def update_project_detail(request,pid):
    template_name = 'projects/update_project_detail.html'
    project = get_object_or_404(Project, pid=pid)
    bc_list = BusinessContact.objects.filter(cid=project.cid)
    pm = project.pm
    if request.method == 'POST':
        form = ProjectUpdateForm(instance=project, data=request.POST)
        if form.is_valid():
            form.save()
            myurl = '/project_detail/{pid}/{cid}/'.format(pid=project.pid,cid=project.cid.cid)
            #myurl = 'http://47.94.224.242:1973/project_detail/{pid}/{cid}/'.format(pid=project.pid,cid=project.cid.cid)
            return HttpResponseRedirect(myurl)
        else:
            username = 'unknown'
            if request.user.is_authenticated():
                username = request.user.username
            print("projects/views.update_project_detail")
            print(username, "FORM NOT VALID")
    else:
        form = ProjectUpdateForm(instance=project)

    return render(request, template_name, {'bc_list':bc_list,'project': project, 'form': form,'pm':pm })

@login_required
def advanced_project_form(request):
    template_name = 'projects/advanced_project_search.html'
    return render(request, template_name)

@login_required
def advanced_project_search(request):
    template_name = 'projects/advanced_project_search_result.html'
    pid = request.GET.get('pid')
    pname = request.GET.get('pname')
    premark = request.GET.get('premark')
    pdetail = request.GET.get('pdetail')
    if not premark:
        premark = ''
    if not pdetail:
        pdetail = ''
    if pid:
        project_list = Project.objects.filter(pid=pid)
        num_of_result = len(project_list)
        return render(request, template_name, {'num_of_result': num_of_result, 'project_list': project_list})
    else:
        project_list = Project.objects.filter(
        pname__contains=pname,
        premark__contains=premark,
        pdetail__contains=pdetail)

        num_of_result = len(project_list)

        if pname:
            project_list = search_sort_pname_helper(project_list, pname)
        return render(request, template_name, {'num_of_result': num_of_result, 'project_list': project_list})

# 以项目名称匹配度排序
def search_sort_pname_helper(proj_list, p):
    new_list = []
    for proj in proj_list:
        index = get_pname_index(proj, p)
        obj = [proj, index]
        new_list.append(obj)

    new_list = sorted(new_list, reverse=True, key=comparator)
    # print(new_list)
    projects = [elem[0] for elem in new_list]
    return projects

def get_pname_index(proj,p):
    project_len = len(proj.pname)
    str_count = len(proj.pname.split(p)) - 1
    #print(str_count)
    if(project_len == 0):
        return 0
    else:
        index = str_count/project_len
        return index

def comparator(elem):
    return elem[1]

# 专家账单筛选，起止时间
def search_interview_by_time(request):
    q = request.GET.get('q')
    list = search_by_time_helper(q)
    #print(len(list))
    return render(request, 'projects/interview_search_result.html', {'q':q,'list': list,})

# 客户账单筛选，客户公司名称和起止时间
def search_client_project_by_time(request):
    time = request.GET.get('time')
    client_name = request.GET.get('client_name')
    error_msg = 'none'
    if not time and not client_name:
        error_msg = 'error'
        return render(request, 'projects/client_project_search_result.html', {'time': time, 'error_msg': error_msg,})
    else:
        list = []
        if not client_name:
            list_time = search_by_time_helper(time)
            list = list_time
        if not time:
            print(client_name)
            list_client = search_by_cnmae_helper(client_name)

            list = list_client
        else:
            #print("双重限制")
            """
            list_time = search_by_time_helper(time)
            for elem in list_time:
                if client_name in elem.pid.cid.cname:
                    list.append(elem)
            """
            list_time = set(search_by_time_helper(time))
            list_client = set(search_by_cnmae_helper(client_name))
            list = list_time & list_client

        return render(request, 'projects/client_project_search_result.html', {'error_msg': error_msg, 'list': list })

# 起止时间筛选
def search_by_time_helper(time):
    time = time.split()
    #print("--------------", time)
    start = time[0]
    end = get_today_date()
    if len(time) > 1:
        end = time[1]
    #print("--------------", start, end)
    list = Project2Expert.objects.filter(itv_date__gte=start, itv_date__lte=end)
    return list

# format当天日期
def get_today_date():
    year = timezone.now().year
    month = timezone.now().month
    if month < 10:
        month = '0{m}'.format(m=month)
    day = timezone.now().day
    if day < 10:
        day = '0{d}'.format(d=day)
    date = "{y}-{m}-{d}".format(y=year, m=month, d=day)
    return date

# 客户账单，客户公司名称筛选
def search_by_cnmae_helper(client_name):
    clients = Client.objects.filter(cname__contains=client_name)

    projects = []
    for client in clients:
        projects_per_client = Project.objects.filter(cid=client)
        projects = chain(projects_per_client, projects)  # 合并

    list = []
    for project in projects:
        temp = Project2Expert.objects.filter(pid=project)
        list = chain(list,temp)
    return list

