
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from experts.models import *
from clients.models import Client, BusinessContact, FinancialContact
from projects.models import Project
from .forms import ClientForm

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def client(request):
    return render(request, 'clients/client_base.html')

def client_info_list(request):
    clients_list = Client.objects.all()
    paginator = Paginator(clients_list, 30)
    page = request.GET.get('page')
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)
    return render(request, 'clients/client_info_list.html', {'page':page, 'clients':clients})

def client_detail(request, cid):
    print("===========clients/views.client_detail=========")
    client = get_object_or_404(Client, cid=cid)
    project = Project.objects.filter(cid=client)
    p2es = get_object_or_404(Project, pid=project.pid).expertinfos.all()
    return render(request, 'clients/client_detail.html', {'project': project, 'client': client, 'p2es': p2es})


@login_required
def add_client(request):
    form = ClientForm()
    return render(request, 'clients/add_client.html', {'form': form})




@login_required
def addClientToDatabase(request):
    if request.method == "POST":
        clientInfo_form = ClientForm(data=request.POST)
        if clientInfo_form.is_valid():
            new_client = clientInfo_form.save(commit=False)
            # filter得到的是一个list，而不是一个object
            print(new_client, type(new_client.bc_id), type(new_client.fc_id))
            client = Client.objects.filter(cname=new_client.cname)
            if client.exists() == 0:
                new_project = clientInfo_form.save()
            else:
                print("!!!!!!!!!!!This project already existed!!!!!!!!")
                #return render(request, 'projects/expert_already_exist.html')
        else:
            print("=============views.addClientToDatabase======")
            print("-----------NOT VALID----------")
    else:
        print("!!!!!!!!!!!GET!!!!!!!!")

    # 重定向
    return HttpResponseRedirect('/addcomplete/')

