
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from experts.models import *
from clients.models import Client, BusinessContact, FinancialContact
from projects.models import Project
from .forms import ClientForm,BCForm,FCForm,ClientUpdateForm
from projects.forms import ProjectForm

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


"""
删除功能的view：
delete_client，delete_client_bc，delete_client_fc
"""
@login_required
def delete_client(request, cid):
    template_name = 'clients/client_detail.html'
    client = Client.objects.get(cid=cid)
    result = client.delete()
    if result:
        return HttpResponseRedirect('/client_info_list/')
    else:
        result = '删除失败'
    return render(request, template_name,{'result':result})

@login_required
def delete_client_bc(request, bc_id,cid):
    template_name = 'clients/client_detail.html'
    bc = BusinessContact.objects.get(bc_id=bc_id)
    result = bc.delete()
    if result:
        myurl = "/clients/{cid}/detail".format(cid=cid)
        #myurl = "http://47.94.224.242:1973/clients/{cid}/detail".format(cid=cid)
        return HttpResponseRedirect(myurl)
    else:
        result = '删除失败'
    return render(request, template_name,{'result':result})

@login_required
def delete_client_fc(request, fc_id,cid):
    template_name = 'clients/client_detail.html'
    fc = FinancialContact.objects.get(fc_id=fc_id)
    result = fc.delete()
    if result:
        myurl = "/clients/{cid}/detail".format(cid=cid)
        #myurl = "http://47.94.224.242:1973/clients/{cid}/detail".format(cid=cid)
        return HttpResponseRedirect(myurl)
    else:
        result = '删除失败'
    return render(request, template_name,{'result':result})

"""
在网页上没有入口的一个view，对应的url是/clients/
"""
def client(request):
    return render(request, 'clients/client_base.html')

"""
客户列表
只显示100个客户，每页展示20个
"""
@login_required
def client_info_list(request):
    clients_list = Client.objects.all()[:100]
    paginator = Paginator(clients_list, 20)
    page = request.GET.get('page')
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)
    return render(request, 'clients/client_info_list.html', {'page':page, 'clients':clients})

"""
客户详情页
"""
@login_required
def client_detail(request, cid):
    client = get_object_or_404(Client, cid=cid)
    projects = Project.objects.filter(cid=client)    # 该客户的所有项目
    bc_list = BusinessContact.objects.filter(cid=client)    #该客户的所有业务联系人
    fc_list = FinancialContact.objects.filter(cid=client)    #该客户的所有财务联系人

    experts = []
    #if len(projects) > 0:
    #    print("===========clients/views.client_detail/该客户有projects=========")
    #    for project in projects:
            # 获取与该客户合作过的所有专家
    #        experts += project.expertinfos.all()
    #   return render(request, 'clients/client_detail.html', {'projects': projects, 'client': client, 'experts': experts,'bc_list':bc_list,'fc_list':fc_list})
    #print("===========clients/views.client_detail/该客户无projects=========")
    return render(request, 'clients/client_detail.html', {'projects': projects, 'client': client, 'experts': experts,'bc_list':bc_list,'fc_list':fc_list})


"""
从客户页面添加项目
"""
@login_required
def client_add_project(request, cid):
    form = ProjectForm()
    client = Client.objects.get(cid=cid)
    bc_list = BusinessContact.objects.filter(cid=client)    #获取客户方所有业务联系人
    result = {}
    if request.method == "POST":
        pname = request.POST.get('pname')
        pm = request.POST.get('pm')
        person_in_charge = request.POST.get('person_in_charge')
        pcreatetime = request.POST.get('pcreatetime')
        pdeadline = request.POST.get('pdeadline')
        premark = request.POST.get('premark')

        project = Project.objects.filter(pname=pname, cid=client)    #同一个客户不可添加同名项目
        if project.exists() == 0:
            new_project = Project()
            new_project.cid = client
            new_project.pname = pname
            new_project.cname = client.cname
            new_project.pm = pm
            new_project.person_in_charge = person_in_charge
            new_project.pcreatetime = pcreatetime
            new_project.pdeadline = pdeadline
            new_project.premark = premark
            new_project.save()
            result['status'] = 'success'
            myurl = "/clients/{cid}/detail".format(cid=cid)
            #print(new_project)
            #myurl = "http://47.94.224.242:1973/clients/{cid}/detail".format(cid=cid)
            return HttpResponseRedirect(myurl)

        else:
            #print("!!!!!!!!!!!This project already existed!!!!!!!!")
            result['status'] = 'error'
    else:
        #print("!!!!!!!!!!!GET!!!!!!!!")
        pass
    return render(request, 'clients/client_add_project.html', {'bc_list':bc_list,'form': form,'client':client,'result':result})

"""
添加客户
"""
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
            client = Client.objects.filter(cname=new_client.cname)    # 不可添加同名客户
            if client.exists() == 0:
                new_client = clientInfo_form.save()
                if new_client.bc_name != '':
                    BusinessContact.objects.create(bc_name=new_client.bc_name,cid=new_client)
                if new_client.fc_name != '':
                    FinancialContact.objects.create(fc_name=new_client.fc_name,cid=new_client)
                #myurl = "http://127.0.0.1:8000/clients/{cid}/detail".format(cid=new_client.cid)
                myurl = "/clients/{cid}/detail".format(cid=new_client.cid)
                #myurl = "http://47.94.224.242:1973/clients/{cid}/detail".format(cid=new_client.cid)
                return HttpResponseRedirect(myurl)
            else:
                # 如果存在同名客户会自动跳转到该客户详情页
                c = client.first()
                myurl = "/clients/{cid}/detail".format(cid=c.cid)
                #myurl = "http://47.94.224.242:1973/clients/{cid}/detail".format(cid=c.cid)
                return HttpResponseRedirect(myurl)
        else:
            print("=============views.addClientToDatabase======")
            print("-----------NOT VALID----------")
    else:
        pass
        #print("!!!!!!!!!!!GET!!!!!!!!")
    # 重定向
    return HttpResponseRedirect('/client_info_list/')

"""
更新客户
"""
def update_client_detail(request,cid):
    template_name = 'clients/update_client_detail.html'
    client = get_object_or_404(Client, cid=cid)
    bc_list = BusinessContact.objects.filter(cid=client)
    fc_list = FinancialContact.objects.filter(cid=client)
    result = {}
    if request.method == 'POST':
        form = ClientUpdateForm(instance=client, data=request.POST)
        if form.is_valid():
            form.save()
            result['status'] = 'success'
            myurl = "/clients/{cid}/detail".format(cid=cid)
            #myurl = "http://47.94.224.242:1973/clients/{cid}/detail".format(cid=cid)
            return HttpResponseRedirect(myurl)
        else:
            result['status'] = 'error'
    else:
        form = ClientUpdateForm(instance=client)

    return render(request, template_name, {'client': client, 'form': form,'bc_list':bc_list,'fc_list':fc_list,'result':result })


"""
添加/更新 业务/财务联系人
"""
def client_add_bc(request, cid):
    template_name = 'clients/add_bc.html'
    result = {}
    if request.method == 'POST':
        form = BCForm(data=request.POST)
        bc_name = request.POST.get('bc_name')
        bc_gender = request.POST.get('bc_gender')
        bc_mobile = request.POST.get('bc_mobile')
        bc_wechat = request.POST.get('bc_wechat')
        bc_email = request.POST.get('bc_email')
        bc_position = request.POST.get('bc_position')
        if form.is_valid():
            new_bc = form.save(commit=False)
            bc = BusinessContact.objects.filter(bc_name=new_bc.bc_name)    # 不可添加同名业务联系人
            if bc.exists() == 0:
                new_bc = BusinessContact()
                new_bc.cid_id = cid
                new_bc.bc_name = bc_name
                new_bc.bc_gender = bc_gender
                new_bc.bc_mobile = bc_mobile
                new_bc.bc_wechat = bc_wechat
                new_bc.bc_email = bc_email
                new_bc.bc_position = bc_position
                new_bc.save()
                result['status'] = 'success'
                myurl = "/clients/{cid}/detail".format(cid=cid)
                #myurl = "http://47.94.224.242:1973/clients/{cid}/detail".format(cid=cid)
                return HttpResponseRedirect(myurl)
            else:
                result['status'] = 'error'
        else:
            result['status'] = 'error'
    else:
        form = BCForm()
    return render(request, template_name, {'form': form, 'result': result, })

def client_add_fc(request, cid):
    template_name = 'clients/add_fc.html'
    result = {}
    if request.method == 'POST':
        form = FCForm(data=request.POST)
        fc_name = request.POST.get('fc_name')
        fc_gender = request.POST.get('fc_gender')
        fc_mobile = request.POST.get('fc_mobile')
        fc_wechat = request.POST.get('fc_wechat')
        fc_email = request.POST.get('fc_email')
        fc_position = request.POST.get('fc_position')
        if form.is_valid():
            new_fc = form.save(commit=False)
            fc = FinancialContact.objects.filter(fc_name=new_fc.fc_name)    # 不可添加同名财务联系人
            if fc.exists() == 0:
                new_fc = FinancialContact()
                new_fc.cid_id = cid
                new_fc.fc_name = fc_name
                new_fc.fc_gender = fc_gender
                new_fc.fc_mobile = fc_mobile
                new_fc.fc_wechat = fc_wechat
                new_fc.fc_email = fc_email
                new_fc.fc_position = fc_position
                new_fc.save()
                result['status'] = 'success'
                myurl = "/clients/{cid}/detail".format(cid=cid)
                #myurl = "http://47.94.224.242:1973/clients/{cid}/detail".format(cid=cid)
                return HttpResponseRedirect(myurl)
            else:
                result['status'] = 'error'
        else:
            result['status'] = 'error'

    else:
        form = FCForm()
    return render(request, template_name, {'form': form, 'result': result, })

def bc_detail_update(request, bc_id, cid):
    template_name = 'clients/add_bc.html'
    result = {}
    if bc_id:
        object = get_object_or_404(BusinessContact, bc_id=bc_id)

        if request.method == 'POST':
            form = BCForm(instance=object, data=request.POST)
            if form.is_valid():
                form.save()
                result['status'] = 'success'
                myurl = "/clients/{cid}/detail".format(cid=cid)
                #myurl = "http://47.94.224.242:1973/clients/{cid}/detail".format(cid=cid)
                return HttpResponseRedirect(myurl)
            else:
                result['status'] = 'error'
        else:
            form = BCForm(instance=object)

    return render(request, template_name, {'bc':object,'form': form,'result':result, })

def fc_detail_update(request, fc_id, cid):
    template_name = 'clients/add_fc.html'
    result = {}
    if fc_id:
        object = get_object_or_404(FinancialContact, fc_id=fc_id)

        if request.method == 'POST':
            form = FCForm(instance=object, data=request.POST)
            if form.is_valid():
                form.save()
                result['status'] = 'success'
                myurl = "/clients/{cid}/detail".format(cid=cid)
                #myurl = "http://47.94.224.242:1973/clients/{cid}/detail".format(cid=cid)
                return HttpResponseRedirect(myurl)
            else:
                result['status'] = 'error'
        else:
            form = FCForm(instance=object)


    return render(request, template_name, {'fc': object, 'form': form, 'result': result, })

"""
搜索客户
搜索词为名称，搜索结果按"相似指数"排序
"""
def advanced_client_form(request):
    template_name = 'clients/advanced_client_search.html'
    return render(request, template_name)

def advanced_client_search(request):
    template_name = 'clients/advanced_client_search_result.html'

    cname = request.GET.get('cname')

    if not cname:
        cname = ''

    client_list = Client.objects.filter(cname__contains=cname)
    num_of_result = len(client_list)
    client_list = search_sort_cname_helper(client_list, cname)

    return render(request, template_name, {'num_of_result': num_of_result, 'client_list': client_list})


def search_sort_cname_helper(client_list, c):
    new_list = []
    for client in client_list:
        index = get_cname_index(client, c)
        obj = [client, index]
        new_list.append(obj)

    new_list = sorted(new_list, reverse=True, key=comparator)
    projects = [elem[0] for elem in new_list]
    return projects

def get_cname_index(client,c):
    client_len = len(client.cname)
    str_count = len(client.cname.split(c)) - 1
    if(client_len == 0):
        return 0
    else:
        index = str_count/client_len
        return index

def comparator(elem):
    return elem[1]