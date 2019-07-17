
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from experts.models import *
from clients.models import Client, BusinessContact, FinancialContact
from projects.models import Project
from .forms import ClientForm,BCForm,FCForm

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
    projects = Project.objects.filter(cid=client)
    experts = []
    if len(projects) > 0:
        print("===========clients/views.client_detail/该客户有projects=========")
        for project in projects:
            experts += project.expertinfos.all()
        return render(request, 'clients/client_detail.html', {'projects': projects, 'client': client, 'experts': experts})
    print("===========clients/views.client_detail/该客户无projects=========")
    return render(request, 'clients/client_detail.html', {'projects': projects, 'client': client, 'experts': experts})


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
            client = Client.objects.filter(cname=new_client.cname)
            if client.exists() == 0:
                new_client = clientInfo_form.save()
                if new_client.bc_name != '':
                    BusinessContact.objects.create(bc_name=new_client.bc_name,cid=new_client)
                if new_client.fc_name != '':
                    FinancialContact.objects.create(fc_name=new_client.fc_name,cid=new_client)

                #myurl = "http://127.0.0.1:8000/clients/{cid}/detail".format(cid=new_client.cid)
                myurl = "http://47.94.224.242:197/clients/{cid}/detail".format(cid=new_client.cid)
                return HttpResponseRedirect(myurl)
            else:
                #print("!!!!!!!!!!!This project already existed!!!!!!!!")
                c = client.first()
                #myurl = "http://127.0.0.1:8000/clients/{cid}/detail".format(cid=c.cid)
                myurl = "http://47.94.224.242:197/clients/{cid}/detail".format(cid=new_client.cid)
                return HttpResponseRedirect(myurl)
        else:
            print("=============views.addClientToDatabase======")
            print("-----------NOT VALID----------")
    else:
        print("!!!!!!!!!!!GET!!!!!!!!")
    # 重定向
    return HttpResponseRedirect('/client_info_list/')


def bc_detail_update(request, bc_id, cid):
    print("---------------bc_detail_update------------")
    template_name = 'clients/add_bc.html'
    object = get_object_or_404(BusinessContact, bc_id=bc_id)
    result = {}
    if request.method == 'POST':
        form = BCForm(instance=object, data=request.POST)
        if form.is_valid():
            print("valid????")
            form.save()
            result['status'] = 'success'
            #myurl = "http://127.0.0.1:8000/clients/{cid}/detail/".format(cid=cid)
            #myurl = "http://47.94.224.242:1973/{ename}/{eid}/".format(ename=ename, eid=eid)
            #return HttpResponseRedirect(myurl)
    else:
        form = BCForm(instance=object)

    return render(request, template_name, {'bc':object,'form': form,'result':result, })

def fc_detail_update(request, fc_id, cid):
    print("---------------fc_detail_update------------")
    template_name = 'clients/add_fc.html'
    object = get_object_or_404(FinancialContact, fc_id=fc_id)

    if request.method == 'POST':
        form = FCForm(instance=object, data=request.POST)
        if form.is_valid():
            form.save()
            # if is_ajax(), we just return the validated form, so the modal will close
            #myurl = "http://127.0.0.1:8000/client_detail/{cid}/".format(cid=cid)
            #myurl = "http://47.94.224.242:1973/{ename}/{eid}/".format(ename=ename, eid=eid)
            #return HttpResponseRedirect(myurl)
    else:
        form = FCForm(instance=object)

    return render(request, template_name, {'bc':object,'form': form,})