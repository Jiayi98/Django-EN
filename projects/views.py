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

    # 删除一次访谈记录，对应专家的访谈次数字段更新
    expert = p2e.eid
    expert.interview_num = expert.interview_num - 1
    expert.save()

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

def project_detail(request, pid, cid):
    project = get_object_or_404(Project, pid=pid)
    client = Client.objects.filter(cid=cid).first()
    experts = get_object_or_404(Project, pid=pid).expertinfos.all().distinct()

    p2es = Project2Expert.objects.filter(pid=pid)
    return render(request, 'projects/project_detail.html', {'experts':experts,'project': project, 'client': client, 'p2es': p2es,'createtime':project.pcreatetime})



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
                new_obj = Project2Expert.objects.create(eid=expert,pid=project,c_payment=0.0,e_payment=0.0)
                myurl = '/projects/update_p2e_detail/{pteid}/'.format(pteid=new_obj.pteid)
                return HttpResponseRedirect(myurl)
                #return render(request, 'projects/add_p2e.html', {"project": project, "form": form,"new_obj":new_obj})
            else:
                flag['status'] = 'error'
    return render(request, 'projects/add_p2e.html', {"project": project, "form": form,'flag':flag})

def update_p2e_detail(request,pteid):
    object = get_object_or_404(Project2Expert, pteid=pteid)
    #print(type(object.pid),type(object.eid))
    result = {}
    if request.method == 'POST':
        form = Project2ExpertForm(instance=object, data=request.POST)
        if form.is_valid():

            form.save()
            result['status'] = 'success'
            myurl = 'http://127.0.0.1:8000/project_detail/{pid}/{cid}/'.format(pid=object.pid.pid, cid=object.pid.cid.cid)
            #myurl = 'http://47.94.224.242:1973/project_detail/{pid}/{cid}/'.format(pid=object.pid.pid, cid=object.pid.cid.cid)
            return HttpResponseRedirect(myurl)
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

def update_project_detail(request,pid):
    template_name = 'projects/update_project_detail.html'
    project = get_object_or_404(Project, pid=pid)
    bc_list = BusinessContact.objects.filter(cid=project.cid)
    if request.method == 'POST':
        form = ProjectUpdateForm(instance=project, data=request.POST)
        if form.is_valid():
            form.save()
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