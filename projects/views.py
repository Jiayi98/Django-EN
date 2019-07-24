from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from experts.models import ExpertInfo,WorkExp
from clients.models import Client,BusinessContact
from projects.models import Project
from .forms import *

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
"""
def pm_contact_info(request,pid):
    #template_name = 'projects/pm_contact_info.html'
    template_name = 'projects/project_detail.html'
    #try:
    #    project = get_object_or_404(Project, pid=pid)
    #except:
    #    HttpResponseRedirect()
    #else:
    #    msg = 'success'
    #    if request.user.has_perm('查看项目经理联系方式'):
    #        # print("有权限")
    #        # print("=============views.expert_contact_info======")
                # template_name = 'projects/pm_contact_info.html'
    #        msg = 'success'
    #    else:
    #        # print("无权限")
    #        # template_name = 'projects/pm_info.html'
    #        msg = "error"
    return render(request, template_name, {'project': project})


def pm_contact_info_update(request, pid):
    template_name = 'projects/update_pm_contact_info.html'
    object = get_object_or_404(Project, pid=pid)

    if request.method == 'POST':
        form = PMContactInfoUpdateDB(instance=object, data=request.POST)
        if form.is_valid():
            form.save()
            myurl = 'http://127.0.0.1:8000/project_detail/{pid}/{cid}/'.format(pid=pid, cid=object.cid.cid)
            #myurl = 'http://47.94.224.242:1973/project_detail/{pid}/{cid}/'.format(pid=object.pid.pid, cid=object.pid.cid.cid)
            return HttpResponseRedirect(myurl)
    else:
        form = PMContactInfoUpdateDB(instance=object)

    return render(request, template_name, {'project': object, 'form': form, })
"""
@login_required
def delete_project(request, pid):
    print("=============project/views.delete======")
    template_name = 'projects/project_detail.html'
    project = Project.objects.get(pid=pid)
    result = project.delete()
    if result:
        return HttpResponseRedirect('/project_info_list/')
    else:
        result = '删除失败'
    return render(request, template_name,{'result':result})

@login_required
def delete_p2e(request, pteid, pid):
    print("=============project/views.delete======")
    template_name = 'projects/project_detail.html'
    p2e = Project2Expert.objects.get(pteid=pteid)
    project = Project.objects.get(pid=pid)
    result = p2e.delete()
    if result:
        myurl = 'http://127.0.0.1:8000/project_detail/{pid}/{cid}/'.format(pid=pid, cid=project.cid.cid)
        # myurl = 'http://47.94.224.242:1973/project_detail/{pid}/{cid}/'.format(pid=object.pid.pid, cid=object.pid.cid.cid)
        return HttpResponseRedirect(myurl)
    else:
        result = '删除失败'
    return render(request, template_name,{'result':result})

@login_required
def project(request):
    return render(request, 'projects/project_base.html')

def project_info_list(request):
    projects_list = Project.objects.all()
    paginator = Paginator(projects_list, 30)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'projects/project_info_list.html', {'page':page, 'projects':projects})

def project_detail(request, pid, cid):
    print("===========projects/views.project_detail=========")

    project = get_object_or_404(Project, pid=pid)
    createtime = ' {year}-{mon}-{day}'.format(year=project.pcreatetime.year,mon=project.pcreatetime.month, day=project.pcreatetime.day)
    client = Client.objects.filter(cid=cid).first()
    experts = get_object_or_404(Project, pid=pid).expertinfos.all().distinct()

    p2es = Project2Expert.objects.filter(pid=pid)
    return render(request, 'projects/project_detail.html', {'experts':experts,'project': project, 'client': client, 'p2es': p2es,'createtime':createtime})



def add_p2e(request,pid):
    form = P2EForm(data=request.POST)
    project = Project.objects.get(pid=pid)
    ename = request.POST.get('ename')
    eid_num = request.POST.get("eid")
    flag = {}
    if request.method == "POST":
        try:
            expert = ExpertInfo.objects.get(eid=eid_num)
            print("===========projects/views.valid=========")
            #print(eid_num, expert)
        except:
            flag['status'] = 'error'
        else:
            if not ename or expert.ename == ename:
                expert.interview_num = expert.interview_num + 1
                expert.save()
                temp = Project2Expert.objects.filter(eid=expert,pid=project)
                new_obj = Project2Expert.objects.create(eid=expert,pid=project)
                myurl = '/projects/update_p2e_detail/{pteid}/'.format(pteid=new_obj.pteid)
                return HttpResponseRedirect(myurl)
                #return render(request, 'projects/add_p2e.html', {"project": project, "form": form,"new_obj":new_obj})
            else:
                flag['status'] = 'error'
    return render(request, 'projects/add_p2e.html', {"project": project, "form": form,'flag':flag})

def update_p2e_detail(request,pteid):

    object = get_object_or_404(Project2Expert, pteid=pteid)
    #print(type(object.pid),type(object.eid))
    company = WorkExp.objects.filter(eid=object.eid.eid).first()
    if company:
        company = company.company
    else:
        company = '未知'
    result = {}
    if request.method == 'POST':
        form = Project2ExpertForm(instance=object, data=request.POST)
        if form.is_valid():
            #print("valid????")
            object.pname = object.pid.pname
            object.ename = object.eid.ename
            object.ecompany = company
            object.save()
            form.save()
            result['status'] = 'success'
            myurl = 'http://127.0.0.1:8000/project_detail/{pid}/{cid}/'.format(pid=object.pid.pid, cid=object.pid.cid.cid)
            #myurl = 'http://47.94.224.242:1973/project_detail/{pid}/{cid}/'.format(pid=object.pid.pid, cid=object.pid.cid.cid)
            return HttpResponseRedirect(myurl)
    else:
        form = Project2ExpertForm(instance=object)

    return render(request, 'projects/update_p2e_detail.html', {'object': object,'project':object.pid,'expert':object.eid,'company':company,'form': form, 'result': result, })

@login_required
def add_project(request):
    form = ProjectForm()
    return render(request, 'projects/add_project.html', {'form': form})


@login_required
def addProjectToDatabase(request):
    if request.method == "POST":
        pname = request.POST.get('pname')
        cname = request.POST.get('cname')
        pm = request.POST.get('pm')
        pm_mobile = request.POST.get('pm_mobile')
        pm_email = request.POST.get('pm_email')
        pm_wechat = request.POST.get('pm_wechat')
        pm_gender = request.POST.get('pm_gender')
        pdeadline = request.POST.get('pdeadline')
        premark = request.POST.get('premark')
        person_in_charge = request.POST.get('person_in_charge')
        pdetail = request.POST.get('pdetail')
        cid_num = request.POST.get('cid')
        print('---------',cid_num)
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
                new_project.cname = client.cname
                new_project.pm = pm
                new_project.pm_mobile = pm_mobile
                new_project.pm_email = pm_email
                new_project.pm_wechat = pm_wechat
                new_project.pm_gender = pm_gender
                new_project.pdeadline = pdeadline
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

def update_project_detail(request,pid):
    template_name = 'projects/update_project_detail.html'
    project = get_object_or_404(Project, pid=pid)
    bc_list = BusinessContact.objects.filter(cid=project.cid)
    if request.method == 'POST':
        form = ProjectUpdateForm(instance=project, data=request.POST)
        if form.is_valid():
            form.save()
            # if is_ajax(), we just return the validated form, so the modal will close
            myurl = 'http://127.0.0.1:8000/project_detail/{pid}/{cid}/'.format(pid=project.pid,cid=project.cid.cid)
            #myurl = 'http://47.94.224.242:1973/project_detail/{pid}/{cid}/'.format(pid=project.pid,cid=project.cid.cid)
            return HttpResponseRedirect(myurl)
    else:
        form = ProjectUpdateForm(instance=project)

    return render(request, template_name, {'bc_list':bc_list,'project': project, 'form': form, })

def advanced_project_form(request):
    template_name = 'projects/advanced_project_search.html'
    return render(request, template_name)

def advanced_project_search(request):
    template_name = 'projects/advanced_project_search_result.html'
    pid = request.GET.get('pid')
    pname = request.GET.get('pname')
    cname = request.GET.get('cname')
    premark = request.GET.get('premark')
    pdetail = request.GET.get('pdetail')
    #print(type(pname),type(cname),type(premark),type(pdetail))
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
        cname__contains=cname,
        pname__contains=pname,
        premark__contains=premark,
        pdetail__contains=pdetail)

        num_of_result = len(project_list)

        if pname and not cname:
            project_list = search_sort_pname_helper(project_list, pname)
        elif cname and not pname:
            project_list = search_sort_cname_helper(project_list, cname)
        elif pname and cname:
            project_list = search_sort_p_c_helper(project_list, pname ,cname)
        return render(request, template_name, {'num_of_result': num_of_result, 'project_list': project_list})


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

def search_sort_cname_helper(proj_list, c):
    new_list = []
    for proj in proj_list:
        index = get_index(proj, c)
        obj = [proj, index]
        new_list.append(obj)

    new_list = sorted(new_list, reverse=True, key=comparator)
    # print(new_list)
    projects = [elem[0] for elem in new_list]
    return projects

def get_cname_index(proj,c):
    client_len = len(proj.cname)
    str_count = len(proj.cname.split(c)) - 1
    #print(str_count)
    if(client_len == 0):
        return 0
    else:
        index = str_count/client_len
        return index

def search_sort_p_c_helper(proj_list, p,c):
    new_list = []
    for proj in proj_list:
        index = get_p_c_index(proj, p,c)
        obj = [proj, index]
        new_list.append(obj)

    new_list = sorted(new_list, reverse=True, key=comparator)
    # print(new_list)
    projects = [elem[0] for elem in new_list]
    return projects

def get_p_c_index(proj,p,c):
    project_len = len(proj.pname)
    client_len = len(proj.cname)
    p_str_count = len(proj.pname.split(p)) - 1
    c_str_count = len(proj.cname.split(c)) - 1
    #print(str_count)
    if(project_len == 0 and client_len == 0):
        return 0
    else:
        index = (p_str_count+c_str_count)/(project_len+client_len)
        return index

def comparator(elem):
    return elem[1]