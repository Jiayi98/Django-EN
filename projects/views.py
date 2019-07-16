from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from experts.models import ExpertInfo
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
    client = Client.objects.filter(cid=cid)
    p2es = get_object_or_404(Project, pid=pid).expertinfos.all()
    return render(request, 'projects/project_detail.html', {'project': project, 'client': client, 'p2es': p2es})

@login_required
def add_project(request):
    form = ProjectForm()
    return render(request, 'projects/add_project.html', {'form': form})


@login_required
def addProjectToDatabase(request):
    if request.method == "POST":
        projectInfo_form = ProjectForm(data=request.POST)
        if projectInfo_form.is_valid():
            new_project = projectInfo_form.save(commit=False)
            # filter得到的是一个list，而不是一个object
            print(type(new_project.cid))
            project = Project.objects.filter(pname=new_project.ename, cid=new_project.cid.cid, eemail=new_project.pm)
            if project.exists() == 0:
                new_project = projectInfo_form.save()
            else:
                print("!!!!!!!!!!!This project already existed!!!!!!!!")
                #return render(request, 'projects/expert_already_exist.html')
        else:
            print("=============views.addExpertToDatabase======")
            print("-----------NOT VALID----------")
    else:
        print("!!!!!!!!!!!GET!!!!!!!!")

    # 重定向
    return HttpResponseRedirect('/addcomplete/')
