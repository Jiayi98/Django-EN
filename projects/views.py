from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from experts.models import ExpertInfo,WorkExp
from clients.models import Client
from projects.models import Project
from .forms import *

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
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
    client = Client.objects.filter(cid=cid).first()
    experts = get_object_or_404(Project, pid=pid).expertinfos.all()
    p2es = Project2Expert.objects.filter(pid=pid)
    #print(p2es.first().itv_duration)
    return render(request, 'projects/project_detail.html', {'project': project, 'client': client, 'p2es': p2es})



def add_p2e(request,pid):
    form = P2EForm(data=request.POST)
    project = Project.objects.get(pid=pid)
    ename = request.POST.get('ename')
    eid_num = request.POST.get("eid")
    flag = {}
    if request.method == "POST":
        expert = ExpertInfo.objects.get(eid=eid_num)
        print("===========projects/views.valid=========")
        print(eid_num, expert)
        temp = Project2Expert.objects.filter(eid=expert,pid=project)
        if temp.exists() == 0 and (not ename or expert.ename == ename):
            new_obj = Project2Expert.objects.create(eid=expert,pid=project)
            print('--------------->',new_obj.pteid)
            myurl = '/projects/update_p2e_detail/{pteid}/'.format(pteid=new_obj.pteid)
            return HttpResponseRedirect(myurl)
            #return render(request, 'projects/add_p2e.html', {"project": project, "form": form,"new_obj":new_obj})
        else:
            flag['status'] = 'error'
    return render(request, 'projects/add_p2e.html', {"project": project, "form": form,'flag':flag})

def update_p2e_detail(request,pteid):

    object = get_object_or_404(Project2Expert, pteid=pteid)
    print(type(object.pid),type(object.eid))
    company = WorkExp.objects.filter(eid=object.eid.eid).first()
    if company:
        company = company.company
    else:
        company = '未知'
    result = {}
    if request.method == 'POST':
        form = Project2ExpertForm(instance=object, data=request.POST)
        if form.is_valid():
            print("valid????")
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
        pm_gender = request.POST.get('pm_gender')
        pdeadline = request.POST.get('pdeadline')
        premark = request.POST.get('premark')
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
                new_project.pm_gender = pm_gender
                new_project.pdeadline = pdeadline
                new_project.premark = premark
                new_project.save()

            else:
                print("!!!!!!!!!!!This project already existed!!!!!!!!")

    else:
        print("!!!!!!!!!!!GET!!!!!!!!")

    # 重定向
    return HttpResponseRedirect('/projects_list/')

def update_project_detail(request,pid):
    template_name = 'projects/update_project_detail.html'
    project = get_object_or_404(Project, pid=pid)

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

    return render(request, template_name, {'project': project, 'form': form, })