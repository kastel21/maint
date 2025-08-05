from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.db.models import Q
from vehicle.models import Assessments
from django.http import JsonResponse
from django.http import HttpResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

import json
from django.core import serializers
from django.forms.models import model_to_dict

def afterlogin_view(request):
    return redirect('customer-dashboard')

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/index.html')


#for showing signup/login button for customer
def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/customerclick.html')

#for showing signup/login button for mechanics
def mechanicsclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/mechanicsclick.html')


#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def pcclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('pclogin')

def financeclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('financelogin')


def technicalclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('technicallogin')
































#for checking user customer, mechanic or admin(by sumit)
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()
def is_mechanic(user):
    return user.groups.filter(name='MECHANIC').exists()
def is_finance(user):
    return user.groups.filter(name='finance').exists()
def is_manager(user):
    return user.groups.filter(name='manager').exists()
def is_procurement(user):
    return user.groups.filter(name='procurement').exists()
def is_supplier(user):
    return user.groups.filter(name='supplier').exists()
def is_pc(user):
    return user.groups.filter(name='PC').exists()

def is_tech(user):
    return user.groups.filter(name='tech').exists()


def is_lo(user):
    return user.groups.filter(name='logistics').exists()







@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]

    print('*******************************')
    for c in models.Customer.objects.all():
        
        print(c.lname)
    print('*******************************')
    for enq in enquiry:
        lname = str(enq.customer)[1:].title()
        #customer=models.Customer.objects.get(user_id=request.user.id)
        print(lname)
        print()
        customer=models.Customer.objects.get(lname=lname)
        customers.append(customer)

    dict={
    'total_customer':models.Customer.objects.all().count(),
    'total_mechanic':models.Mechanic.objects.all().count(),
    'total_request':models.Request.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'vehicle/admin_dashboard.html',context=dict)



@login_required(login_url='adminlogin')
def technical_dashboard_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        lname = str(enq.customer)[1:]
        customer=models.Customer.objects.get(lname=lname)
        customers.append(customer)
    dict={
    'total_customer':models.Customer.objects.all().count(),
    'total_mechanic':models.Mechanic.objects.all().count(),
    'total_request':models.Request.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'vehicle/admin_dashboard.html',context=dict)


@login_required(login_url='adminlogin')
def pc_dashboard_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    dict={
    'total_customer':models.Customer.objects.all().count(),
    'total_mechanic':models.Mechanic.objects.all().count(),
    'total_request':models.Request.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'vehicle/admin_dashboard.html',context=dict)


@login_required(login_url='adminlogin')
def finance_dashboard_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    dict={
    'total_customer':models.Customer.objects.all().count(),
    'total_mechanic':models.Mechanic.objects.all().count(),
    'total_request':models.Request.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'vehicle/admin_dashboard.html',context=dict)


def send_requests(_id):
    print('sending gor ',_id)







def pdf_view(request):
    with open('static/12/Mecha/Fiscal_Device_Gateway_API_v7.2_-_clients_WTwSb0M.pdf', 'r') as pdf:
        response = HttpResponse(pdf.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed

























#============================================================================================
# CUSTOMER RELATED views start
#============================================================================================

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_dashboard_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    work_in_progress=models.Request.objects.all().filter(customer=customer.user.username,status='Repairing').count()
    work_completed=models.Request.objects.all().filter(customer=customer.user.username).filter(Q(status="Repairing Done") | Q(status="Released")).count()
    new_request_made=models.Request.objects.all().filter(customer=customer.user.username).filter(Q(status="Pending") | Q(status="Approved")).count()
    bill=models.Request.objects.all().filter(customer=customer.user.username).filter(Q(status="Repairing Done") | Q(status="Released")).aggregate(Sum('cost'))
    print(bill)
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_request_made':new_request_made,
    'bill':bill['cost__sum'],
    'customer':customer,
    }
    return render(request,'vehicle/customer_dashboard.html',context=dict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/customer_request.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_pc)
def pc_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/pc_request.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_lo)
def lo_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/lo_request.html',{'customer':customer})

@login_required(login_url='customerlogin')
@user_passes_test(is_manager)
def manager_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/manager_request.html',{'customer':customer})

@login_required(login_url='customerlogin')
@user_passes_test(is_finance)
def finance_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/finance_request.html',{'customer':customer})

@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def supplier_awards_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/supplier_awards.html',{'customer':customer})

@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def supplier_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/supplier_request.html',{'customer':customer})

@login_required(login_url='customerlogin')
@user_passes_test(is_tech)
def tech_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/tech_request.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_tech)
def tech_pending_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter( Q( Q(technical=request.user.username)) & Q(technical_approved='No') & Q(technical_rejected_date='.') )

    return render(request,'vehicle/tech_view_requests.html',{'customer':customer,'flag1':'pending','enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_tech)
def tech_approved_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter( Q( Q(technical=request.user.username)) & Q(technical_approved='Yes') )

    return render(request,'vehicle/tech_view_requests.html',{'customer':customer,'flag1':'approved','enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_tech)
def tech_rejected_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter( Q( Q(technical=request.user.username)) & Q(technical_approved='No') & ~Q(technical_rejected_date='.') )

    return render(request,'vehicle/tech_view_requests.html',{'customer':customer,'flag1':'rejected','enquiries':enquiries})




@login_required(login_url='customerlogin')
@user_passes_test(is_manager)
def customer_view_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)


    enqs = []

    enquiries=models.Request.objects.all().filter( Q(lab_manager=request.user.username))
    services = models.Service.objects.all().filter(~Q(POP_date = '.'))
    servs = [x.request_id for x in services ]
    print('servs',servs)
    for enquiry in enquiries:
        #print('id',enquiry.id)
        if str(enquiry.id) in servs:
            pass
            #print('kk',enquiry.id)
        else:
            enqs.append(enquiry)





    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/customer_view_request.html',{'customer':customer,'enquiries':enqs})



@login_required(login_url='customerlogin')
@user_passes_test(is_manager)
def manager_view_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    #groups = request.user.groups.get(name='supplier')
    #print(groups,'groups')
    #enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    # if request.user.groups.filter(name='finance').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( status="Approved") & Q(finance_approved='No'))

    # elif request.user.groups.filter(name='procurement').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( finance_approved="Yes") & Q(job_open='No'))
    # elif request.user.groups.filter(name='supplier').exists():

    #     enquiries=models.Request.objects.all().filter(Q(job_open='Yes'))

        
    # else:
    enquiries=models.Request.objects.all().filter( Q( Q(lab_manager=request.user.username)) & Q( status="Pending"))

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/pc_view_request.html',{'customer':customer,'enquiries':enquiries})


#*****************************************************PC and Request*******************************************************************************

@login_required(login_url='customerlogin')
@user_passes_test(is_pc)
def pc_view_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)

    enquiries=models.Request.objects.all().filter( Q( Q(pc=request.user.username)) & Q( pc_approved="No"))

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/pc_view_requests.html',{'customer':customer,'enquiries':enquiries,'flag':'pending'})

@login_required(login_url='customerlogin')
@user_passes_test(is_pc)
def pc_view_approved_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)

    enquiries=models.Request.objects.all().filter( Q( Q(pc=request.user.username)) & Q( pc_approved="Yes"))

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/pc_view_requests.html',{'customer':customer,'enquiries':enquiries,'flag':'approved'})

@login_required(login_url='customerlogin')
@user_passes_test(is_pc)
def pc_view_rejected_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)

    enquiries=models.Request.objects.all().filter( Q( Q(pc=request.user.username)) & ~Q( pc_rejected_date=".") )

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/pc_view_requests.html',{'customer':customer,'enquiries':enquiries,'flag':'rejected'})


@login_required(login_url='customerlogin')
@user_passes_test(is_pc)
def pc_view_completed_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enqs = []

    enquiries=models.Request.objects.all().filter( Q( Q(pc=request.user.username)))
    services = models.Service.objects.all().filter(~Q(POP_date = '.'))
    servs = [x.request_id for x in services ]
    print('servs',servs)
    for enquiry in enquiries:
        #print('id',enquiry.id)
        if str(enquiry.id) in servs:
            enqs.append(enquiry)
            #print('kk',enquiry.id)
            


    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/pc_view_requests.html',{'customer':customer,'enquiries':enqs,'flag':'completed'})


@login_required(login_url='customerlogin')
@user_passes_test(is_pc)
def pc_open_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')
        flag = request.POST.get('flag', '0')


        enquiry=models.Request.objects.get(id=s_id)
        #enquiry.job_open="No"

        subs= models.Assessments.objects.all().filter(job = s_id)

        #enquiry.mechanic=subs.mechanic
        #enquiry.save()
        if 'completed' in flag:
            
            req=models.Request.objects.get(id=s_id)
            service=models.Service.objects.get(request_id=req.id)
            ass=models.Assessments.objects.get(id=req.assessement_id)
            service.values = service.values.replace('#',', ')
            return render(request,'vehicle/pc_open_completed.html',{'customer':customer,'enquiry':req,'sub':ass,'flag':flag,'service':service})
        else:
            return render(request,'vehicle/pc_open_request.html',{'customer':customer,'enquiry':enquiry,'subs':subs,'flag':flag})

    else:
        return redirect('pc-view-request')





@login_required(login_url='customerlogin')
@user_passes_test(is_pc)
def pc_approve_request_view1(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')
        

        enquiry=models.Request.objects.get(id=s_id)
        #enquiry.job_open="No"

        subs= models.Assessments.objects.all().filter(job = s_id)

        #enquiry.mechanic=subs.mechanic
        #enquiry.save()

        return render(request,'vehicle/pc_open_request.html',{'customer':customer,'enquiry':enquiry,'subs':subs})
    else:
        return JsonResponse({'response':'No get response'})







@login_required(login_url='customerlogin')
@user_passes_test(is_pc)
def pc_approves_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':

        r_id = request.POST.get('r_id', '0')
        reasons = request.POST.get('reasons', '')
        now = datetime.now()
        formatted_date_str = now.strftime("%Y-%m-%d")
        enquiry=models.Request.objects.get(id=r_id)

        if reasons != '':
            enquiry.reasons=reasons
            enquiry.pc_approved="No"
            enquiry.pc_rejected_date=formatted_date_str
            enquiry.save()
        else:
            enquiry.pc_approved="Yes"
            enquiry.save()
        return redirect('pc-view-request')
        #return render(request,'vehicle/pc_justify_supplier.html',{'customer':customer,'enquiry':enquiry})
    else:
        return redirect('pc-view-request')

#*********************************************************************TECH and reuqest*****************************************************************************

@login_required(login_url='customerlogin')
@user_passes_test(is_tech)
def tech_view_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    #groups = request.user.groups.get(name='supplier')
    #print(groups,'groups')
    #enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    # if request.user.groups.filter(name='finance').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( status="Approved") & Q(finance_approved='No'))

    # elif request.user.groups.filter(name='procurement').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( finance_approved="Yes") & Q(job_open='No'))
    # elif request.user.groups.filter(name='supplier').exists():

    #     enquiries=models.Request.objects.all().filter(Q(job_open='Yes'))

        
    # else:
    enquiries=models.Request.objects.all().filter(  Q( pc_approved="Yes") & Q(technical_approved="No") )

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/tech_view_requests.html',{'customer':customer,'enquiries':enquiries})




@login_required(login_url='customerlogin')
@user_passes_test(is_tech)
def tech_open_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')
        flag = request.POST.get('flag1', '0')

        enquiry=models.Request.objects.get(id=s_id)
        #enquiry.job_open="No"

        #subs= models.Assessments.objects.all().filter(job = s_id)

        #enquiry.mechanic=subs.mechanic
        #enquiry.save()

        return render(request,'vehicle/tech_open_request.html',{'customer':customer,'enquiry':enquiry, 'flag1':flag})
    else:
        return redirect('tech-view-request')













@login_required(login_url='customerlogin')
@user_passes_test(is_tech)
def tech_approves_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':

        r_id = request.POST.get('r_id', '0')
        reasons = request.POST.get('reasons', '')

        enquiry=models.Request.objects.get(id=r_id)
        enquiry.reasons=reasons
        now = datetime.now()
        formatted_date_str = now.strftime("%Y-%m-%d")
        enquiry.technical_approved="Yes"
        enquiry.technical_approved_date =formatted_date_str
        enquiry.job_open="Yes"
        enquiry.job_open_date=formatted_date_str

        enquiry.save()
        send_notice()
        return redirect('tech-view-request')
        #return render(request,'vehicle/tech_approve_request.html',{'customer':customer,'enquiry':enquiry})
    else:
        return redirect('tech-view-request')









#*********************************************************************finance and reuqest*****************************************************************************

@login_required(login_url='customerlogin')
@user_passes_test(is_finance)
def finance_view_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)

    enquiries=models.Request.objects.all().filter(  Q( pc_approved="Yes") & Q(finance_approved="No") & ~Q(mechanic="None") & Q(technical_approved="Yes") )

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/finance_view_requests.html',{'customer':customer,'enquiries':enquiries,'flag':'0'})

@login_required(login_url='customerlogin')
@user_passes_test(is_finance)
def finance_view_approved_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)

    enquiries=models.Request.objects.all().filter(  Q(finance_approved="Yes") )

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/finance_view_requests.html',{'customer':customer,'enquiries':enquiries,'flag':'2'})

@login_required(login_url='customerlogin')
@user_passes_test(is_finance)
def finance_view_rejected_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)

    enquiries=models.Request.objects.all().filter(  Q(finance_approved="No") & ~Q(finance_rejected_date=".")  )

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/finance_view_requests.html',{'customer':customer,'enquiries':enquiries,'flag':'1'})




@login_required(login_url='customerlogin')
@user_passes_test(is_finance)
def finance_open_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')
        flag = request.POST.get('flag', '0')

        enquiry=models.Request.objects.get(id=s_id)
        #enquiry.job_open="No"

        subs= models.Assessments.objects.get(id = enquiry.assessement_id)

        #enquiry.mechanic=subs.mechanic
        #enquiry.save()

        return render(request,'vehicle/finance_open_request.html',{'customer':customer,'enquiry':enquiry,'sub':subs,'flag':flag})
    else:
        return redirect('finance-view-request')













@login_required(login_url='customerlogin')
@user_passes_test(is_finance)
def finance_approves_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':

        r_id = request.POST.get('r_id', '0')
        reasons = request.POST.get('reasons', '')
        now = datetime.now()
        formatted_date_str = now.strftime("%Y-%m-%d")
        enquiry=models.Request.objects.get(id=r_id)

        if reasons.strip() != '':

            enquiry.reasons=reasons

            enquiry.finance_approved="No"
            enquiry.finance_rejected_date =formatted_date_str

        else:

            enquiry.finance_approved="Yes"
            enquiry.finance_approved_date =formatted_date_str
        # enquiry.job_open="Yes"
        # enquiry.job_open_date=formatted_date_str

        enquiry.save()
        # send_notice()
        return redirect('finance-view-request')
        #return render(request,'vehicle/tech_approve_request.html',{'customer':customer,'enquiry':enquiry})
    else:
        return redirect('finance-view-request')







#*********************************************************************lo and job*****************************************************************************

@login_required(login_url='customerlogin')
@user_passes_test(is_lo)
def lo_view_jobs_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)

    services=models.Service.objects.all().filter(  Q( tech_approved="Yes") & Q(POP_date='.') )


    #enquiries=models.Service.objects.all().filter(  Q( tech_approved="Yes") )







    return render(request,'vehicle/lo_view_jobs.html',{'customer':customer,'enquiries':services,'flag':'0','services':services})

@login_required(login_url='customerlogin')
@user_passes_test(is_lo)
def lo_view_completed_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)

    enquiries=models.Service.objects.all().filter(  ~Q(POP_date='.') & ~Q(POP='') )

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/lo_view_jobs.html',{'customer':customer,'services':enquiries,'flag':'2'})



@login_required(login_url='customerlogin')
@user_passes_test(is_lo)
def lo_open_job_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')
        flag = request.POST.get('flag', '0')
        service=models.Service.objects.get(id=s_id)
        req=models.Request.objects.get(id=service.request_id)
        ass=models.Assessments.objects.get(id=req.assessement_id)
        service.values = service.values.replace('#',', ')

        #enquiry.job_open="No"


        #enquiry.mechanic=subs.mechanic
        #enquiry.save()

        return render(request,'vehicle/lo_open_job.html',{'customer':customer,'enquiry':req,'sub':ass,'flag':flag,'service':service})
    else:
        return redirect('finance-view-request')




import os

@login_required(login_url='customerlogin')
@user_passes_test(is_lo)
def lo_uploads_pop_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
   
    if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            r_id = request.POST.get('s_id', '0')
            service=models.Service.objects.get(id=r_id)

            fs = FileSystemStorage()

            loc = os.path.join(str(r_id),str(service.mechanic))
            loc1 = os.path.join(loc,myfile.name.replace(' ','_'))
            loco = os.path.join('pop',loc1)
            filename = fs.save(loco, myfile)
            uploaded_file_url = fs.url(filename.replace(' ','_'))
            print('saved here',uploaded_file_url)

            now = datetime.now()
            formatted_date_str = now.strftime("%Y-%m-%d")
            service.POP = uploaded_file_url
            service.POP_date = formatted_date_str
            service.save()

            # adminenquiry=forms.FinanceApproveRequestForm(request.POST)
            # if adminenquiry.is_valid():
            #     enquiry_x=models.Request.objects.get(id=pk)
            #     #enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
            #     #enquiry_x.cost=adminenquiry.cleaned_data['cost']
            #     enquiry_x.status=adminenquiry.cleaned_data['status']

            #     enquiry_x.save()
            # else:
            #     print("form is invalid new 1")
            
            #     print(adminenquiry.errors)
            return HttpResponseRedirect('/lo-view-jobs')











@login_required(login_url='customerlogin')
@user_passes_test(is_finance)
def lo_approves_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':

        r_id = request.POST.get('r_id', '0')
        reasons = request.POST.get('reasons', '')
        now = datetime.now()
        formatted_date_str = now.strftime("%Y-%m-%d")
        enquiry=models.Request.objects.get(id=r_id)

        if reasons.strip() != '':

            enquiry.reasons=reasons

            enquiry.finance_approved="No"
            enquiry.finance_rejected_date =formatted_date_str

        else:

            enquiry.finance_approved="Yes"
            enquiry.finance_approved_date =formatted_date_str
        # enquiry.job_open="Yes"
        # enquiry.job_open_date=formatted_date_str

        enquiry.save()
        # send_notice()
        return redirect('finance-view-request')
        #return render(request,'vehicle/tech_approve_request.html',{'customer':customer,'enquiry':enquiry})
    else:
        return redirect('finance-view-request')









#*********************************************************************Supplier and reuqest*****************************************************************************

@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def supplier_view_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    #groups = request.user.groups.get(name='supplier')
    #print(groups,'groups')
    #enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    # if request.user.groups.filter(name='finance').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( status="Approved") & Q(finance_approved='No'))

    # elif request.user.groups.filter(name='procurement').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( finance_approved="Yes") & Q(job_open='No'))
    # elif request.user.groups.filter(name='supplier').exists():

    #     enquiries=models.Request.objects.all().filter(Q(job_open='Yes'))

        
    # else:
    enquiries=models.Request.objects.all().filter(  Q( job_open="Yes") & Q(technical_approved="Yes") )
    asses= Assessments.objects.all().filter(mechanic=customer.user.username)
    asses_jobs = [x.job for x in asses]
    print('asseses', asses_jobs)
    new1 =[]
    for enquiry in enquiries:
        if str(enquiry.id) not in asses_jobs:
            print('adding '+str(enquiry.id),enquiry)
            new1.append(enquiry)

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/supplier_view_requests.html',{'customer':customer,'enquiries':new1})




@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def supplier_open_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')

        enquiry=models.Request.objects.get(id=s_id)
        #enquiry.job_open="No"

        #subs= models.Assessments.objects.all().filter(job = s_id)

        #enquiry.mechanic=subs.mechanic
        #enquiry.save()

        return render(request,'vehicle/supplier_open_request.html',{'customer':customer,'enquiry':enquiry})
    else:
        return redirect('supplier-view-request')




@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def past_awards(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    #groups = request.user.groups.get(name='supplier')
    #print(groups,'groups')
    #enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    # if request.user.groups.filter(name='finance').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( status="Approved") & Q(finance_approved='No'))

    # elif request.user.groups.filter(name='procurement').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( finance_approved="Yes") & Q(job_open='No'))
    # elif request.user.groups.filter(name='supplier').exists():

    #     enquiries=models.Request.objects.all().filter(Q(job_open='Yes'))

        
    # else:
    enquiries=models.Request.objects.all().filter( Q( Q(mechanic=request.user.username)) & Q( supplier_accepted="Yes") & Q(supplier_done="Yes"))

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/past_awards.html',{'customer':customer,'enquiries':enquiries})



@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def pending_awards(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    #groups = request.user.groups.get(name='supplier')
    #print(groups,'groups')
    #enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    # if request.user.groups.filter(name='finance').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( status="Approved") & Q(finance_approved='No'))

    # elif request.user.groups.filter(name='procurement').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( finance_approved="Yes") & Q(job_open='No'))
    # elif request.user.groups.filter(name='supplier').exists():

    #     enquiries=models.Request.objects.all().filter(Q(job_open='Yes'))

        
    # else:
    enquiries=models.Request.objects.all().filter( Q( Q(mechanic=request.user.username)) & Q( supplier_accepted="No") )

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/pending_awards.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def current_awards(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    #groups = request.user.groups.get(name='supplier')
    #print(groups,'groups')
    #enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    # if request.user.groups.filter(name='finance').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( status="Approved") & Q(finance_approved='No'))

    # elif request.user.groups.filter(name='procurement').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( finance_approved="Yes") & Q(job_open='No'))
    # elif request.user.groups.filter(name='supplier').exists():

    #     enquiries=models.Request.objects.all().filter(Q(job_open='Yes'))

        
    # else:
    enquiries=models.Request.objects.all().filter( Q( Q(mechanic=request.user.username)) & Q( supplier_accepted="Yes") & Q(supplier_done="No"))

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/current_awards.html',{'customer':customer,'enquiries':enquiries})






@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def supplier_open_pending_award(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')

        enquiry=models.Request.objects.get(id=s_id)
        #enquiry.job_open="No"

        #subs= models.Assessments.objects.all().filter(job = s_id)

        #enquiry.mechanic=subs.mechanic
        #enquiry.save()

        return render(request,'vehicle/open_pending_award.html',{'customer':customer,'enquiry':enquiry})
    else:
        return redirect('pending-awards')



@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def supplier_open_current_award(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')

        enquiry=models.Request.objects.get(id=s_id)
        #enquiry.job_open="No"

        #subs= models.Assessments.objects.all().filter(job = s_id)

        #enquiry.mechanic=subs.mechanic
        #enquiry.save()

        return render(request,'vehicle/open_current_award.html',{'customer':customer,'enquiry':enquiry})
    else:
        return redirect('supplier-view-request')



@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def supplier_open_past_award(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')

        enquiry=models.Request.objects.get(id=s_id)
        #enquiry.job_open="No"

        #subs= models.Assessments.objects.all().filter(job = s_id)

        #enquiry.mechanic=subs.mechanic
        #enquiry.save()

        return render(request,'vehicle/open_past_award.html',{'customer':customer,'enquiry':enquiry})
    else:
        return redirect('supplier-view-request')







@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def supplier_submits_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
   
    if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            r_id = request.POST.get('r_id', '0')
            assess = request.POST.get('assess', '')

            fs = FileSystemStorage()

            loc = os.path.join(str(r_id),str(request.user.username))
            loc1 = os.path.join(loc,myfile.name.replace(' ','_'))
            loco = os.path.join('quotations',loc1)
            filename = fs.save(loco, myfile)
            uploaded_file_url = fs.url(filename.replace(' ','_'))
            print('saved here',uploaded_file_url)
            #return render(request, 'core/simple_upload.html', {
                #'uploaded_file_url': uploaded_file_url
            #})

            status = request.POST.get('assesment', 'blank')
            req=models.Request.objects.get(id=r_id)

            req.subs = str(int(req.subs)+1)
            req.save()


            

            ass = Assessments()
            now = datetime.now()
            formatted_date_str = now.strftime("%Y-%m-%d")
            ass.job = r_id
            ass.dos = formatted_date_str
            ass.mechanic = request.user.username
            ass.quotation = uploaded_file_url.replace(' ','_')
            ass.assessment=assess
            ass.save()

            # adminenquiry=forms.FinanceApproveRequestForm(request.POST)
            # if adminenquiry.is_valid():
            #     enquiry_x=models.Request.objects.get(id=pk)
            #     #enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
            #     #enquiry_x.cost=adminenquiry.cleaned_data['cost']
            #     enquiry_x.status=adminenquiry.cleaned_data['status']

            #     enquiry_x.save()
            # else:
            #     print("form is invalid new 1")
            
            #     print(adminenquiry.errors)
            return HttpResponseRedirect('/supplier-view-request')






@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def supplier_update_award_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':

        r_id = request.POST.get('r_id', '0')
        reasons = request.POST.get('reasons', '')

        enquiry=models.Request.objects.get(id=r_id)
        enquiry.reasons=reasons
        now = datetime.now()
        formatted_date_str = now.strftime("%Y-%m-%d")
        enquiry.supplier_accepted="Yes"
        enquiry.supplier_accepted_date =formatted_date_str


        enquiry.save()

        send_notice('supplier '+enquiry.mechanic+ " has accepted and started working ")
        return redirect('view-awards')
        #return render(request,'vehicle/tech_approve_request.html',{'customer':customer,'enquiry':enquiry})
    else:
        return redirect('view-awards')



@login_required(login_url='customerlogin')
@user_passes_test(is_supplier)
def supplier_close_award_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method == 'POST' and request.FILES['myfile']:

        r_id = request.POST.get('r_id', '0')
        cos = request.POST.get('cos', '0')

        enquiry=models.Request.objects.get(id=r_id)


   
        myfile = request.FILES['myfile']

        fs = FileSystemStorage()

        loc = os.path.join(str(r_id),str(request.user.username))
        loc1 = os.path.join(loc,myfile.name.replace(' ','_'))
        loco = os.path.join('invoices',loc1)
        filename = fs.save(loco, myfile)
        uploaded_file_url = fs.url(filename.replace(' ','_'))
        print('saved here',uploaded_file_url)
        #return render(request, 'core/simple_upload.html', {
            #'uploaded_file_url': uploaded_file_url
        #})
        service = models.Service()

        req=models.Request.objects.get(id=r_id)

        service.reg_num=req.vehicle_reg
        service.cos=cos
        service.invoice = uploaded_file_url
        service.request_id = r_id

        service.save()


            


        # enquiry.reasons=reasons
        # now = datetime.now()
        # formatted_date_str = now.strftime("%Y-%m-%d")
        # enquiry.supplier_accepted="Yes"
        # enquiry.supplier_accepted_date =formatted_date_str


        # enquiry.save()

        #send_notice('supplier '+req.mechanic+ " has accepted and started working ")
        #return redirect('supplier-awards')
        return render(request,'vehicle/supplier_add_service.html',{'customer':customer,'enquiry':enquiry,'service_id':service.pk})
    else:
        return redirect('view-awards')


@csrf_exempt
def send_record(request):


    if request.method == 'POST':
            print('in try')
            values = request.POST.get('values',default=None)
            service = request.POST.get('service',default=None)
            r_id = request.POST.get('r_id',default=None)
            s_id = request.POST.get('s_id',default=None)
            next_service = request.POST.get('next_service',default=None)

            print('after get')

            f= open("service.txt","w")
            f.write(str(values)+str(0)+str(service))
            f.close()

            record = models.Service.objects.get(id=s_id)
            record.values=values

            record.next_service = next_service
            print('after next')

            record.service = service
            print('after service')

            record.mechanic = request.user.username
            print('after mehanic')

            d = datetime.now()
            print('after date',d)

            record.doc = "{:%B %d, %Y}".format(d)
            print('after date')
            record.save()
            print('after ave')
            return JsonResponse( {'message':"success"})

        
    return JsonResponse({'message':"failed"})





#********************************************************************tech and job done*********************************************************

@login_required(login_url='customerlogin')
@user_passes_test(is_tech)
def tech_view_services_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    ass={}
    reqs={}
    services = models.Service.objects.all().filter(  ~Q(doc='.') & Q(manager_approved='Yes')& Q(tech_approved='No'))
    # for service in services:
    #     ass[service.id] = models.Assessments.objects.get(id=service.assessment_id)
    #     reqs[service.id] = models.Request.objects.get(id=service.request_id)

        #.filter( Q( Q(pc=request.user.username) | Q(lab_manager=request.user.username)) & Q( status="Pending"))


    return render(request,'vehicle/tech_view_services.html',{'customer':customer,'ass':ass,'reqs':reqs,'services':services})




@login_required(login_url='customerlogin')
@user_passes_test(is_tech)
def tech_open_service_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')

        service=models.Service.objects.get(id=s_id)
        req=models.Request.objects.get(id=service.request_id)
        ass=models.Assessments.objects.get(id=req.assessement_id)
        service.values = service.values.replace('#',', ')




        return render(request,'vehicle/tech_open_service.html',{'customer':customer,'service':service,'enquiry':req,'sub':ass})
    return redirect('tech-view-service')



@login_required(login_url='customerlogin')
@user_passes_test(is_tech)
def tech_approves_service_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('s_id', '0')

        enquiry=models.Service.objects.get(id=s_id)
        enquiry.tech_approved="Yes"

        d = datetime.now()

        enquiry.tech_approved_date = "{:%B %d, %Y}".format(d)
        #enquiry.mechanic=subs.mechanic
        enquiry.save()

        return redirect('tech-view-service')
    else:
        return redirect('tech-view-service')




#********************************************************************manager and job*********************************************************

@login_required(login_url='customerlogin')
@user_passes_test(is_manager)
def manager_view_jobs_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    ass={}
    reqs={}
    services = models.Service.objects.all().filter( Q(lab_manager=request.user.username) & ~Q(doc='.') & Q(manager_approved='No'))
    # for service in services:
    #     ass[service.id] = models.Assessments.objects.get(id=service.assessment_id)
    #     reqs[service.id] = models.Request.objects.get(id=service.request_id)

        #.filter( Q( Q(pc=request.user.username) | Q(lab_manager=request.user.username)) & Q( status="Pending"))


    return render(request,'vehicle/manager_view_jobs.html',{'customer':customer,'ass':ass,'reqs':reqs,'services':services})

@login_required(login_url='customerlogin')
@user_passes_test(is_manager)
def manager_open_job_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')

        service=models.Service.objects.get(id=s_id)
        req=models.Request.objects.get(id=service.request_id)
        ass=models.Assessments.objects.get(id=req.assessement_id)
        service.values = service.values.replace('#',', ')




        return render(request,'vehicle/manager_open_job.html',{'customer':customer,'service':service,'enquiry':req,'sub':ass})
    return redirect('manager-view-jobs')



@login_required(login_url='customerlogin')
@user_passes_test(is_manager)
def manager_approves_job_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('s_id', '0')

        enquiry=models.Service.objects.get(id=s_id)
        enquiry.manager_approved="Yes"

        d = datetime.now()

        enquiry.manager_approved_date = "{:%B %d, %Y}".format(d)
        #enquiry.mechanic=subs.mechanic
        enquiry.save()

        return redirect('manager-view-jobs')
    else:
        return redirect('manager-view-jobs')



#*****************************************************************PC and Jobs************************************************************************************


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def pc_view_jobs_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    #groups = request.user.groups.get(name='supplier')
    #print(groups,'groups')
    #enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    # if request.user.groups.filter(name='finance').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( status="Approved") & Q(finance_approved='No'))

    # elif request.user.groups.filter(name='procurement').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( finance_approved="Yes") & Q(job_open='No'))
    # elif request.user.groups.filter(name='supplier').exists():

    #     enquiries=models.Request.objects.all().filter(Q(job_open='Yes'))

        
    # else:
    assessments=models.Assessments.objects.all()

    enquiries=models.Request.objects.all().filter(Q( job_open='No' ) & ~Q( mechanic='None' ) & Q(technical_approved='No')    )
    for enquiry in enquiries:
        subs= models.Assessments.objects.all().filter(job = enquiry.id)
        enquiry.subs = subs.count()
        enquiry.save()
        #.filter( Q( Q(pc=request.user.username) | Q(lab_manager=request.user.username)) & Q( status="Pending"))

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/pc_view_jobs.html',{'customer':customer,'enquiries':enquiries})








@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def pc_view_submissions_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    #groups = request.user.groups.get(name='supplier')
    #print(groups,'groups')
    #enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    # if request.user.groups.filter(name='finance').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( status="Approved") & Q(finance_approved='No'))

    # elif request.user.groups.filter(name='procurement').exists():
    #     enquiries=models.Request.objects.all().filter(  Q( finance_approved="Yes") & Q(job_open='No'))
    # elif request.user.groups.filter(name='supplier').exists():

    #     enquiries=models.Request.objects.all().filter(Q(job_open='Yes'))

        
    # else:
    assessments=models.Assessments.objects.all()

    enquiries=models.Request.objects.all().filter(Q(job_open='Yes'))
    for enquiry in enquiries:
        subs= models.Assessments.objects.all().filter(job = enquiry.id)
        enquiry.subs = subs.count()
        enquiry.save()
        #.filter( Q( Q(pc=request.user.username) | Q(lab_manager=request.user.username)) & Q( status="Pending"))

    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/pc_view_submission.html',{'customer':customer,'enquiries':enquiries})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def pc_open_submissions_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')

        enquiry=models.Request.objects.get(id=s_id)
        #enquiry.job_open="No"

        subs= models.Assessments.objects.all().filter(job = s_id)

        #enquiry.mechanic=subs.mechanic
        #enquiry.save()

        return render(request,'vehicle/pc_open_submission.html',{'customer':customer,'enquiry':enquiry,'subs':subs})
    else:
        return JsonResponse({'response':'No get response'})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def pc_open_job_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('id', '0')

        enquiry=models.Request.objects.get(id=s_id)
        #enquiry.job_open="No"

        subs= models.Assessments.objects.all().filter(job = s_id)

        #enquiry.mechanic=subs.mechanic
        #enquiry.save()

        return render(request,'vehicle/pc_open_job.html',{'customer':customer,'enquiry':enquiry,'sub':subs})
    else:
        return JsonResponse({'response':'No get response'})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def pc_justify_supplier_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('s_id', '0')
        r_id = request.POST.get('r_id', '0')

        enquiry=models.Request.objects.get(id=r_id)
        #enquiry.job_open="No"

        subs= models.Assessments.objects.get(id = s_id)

        #enquiry.mechanic=subs.mechanic
        #enquiry.save()

        return render(request,'vehicle/pc_justify_supplier.html',{'customer':customer,'enquiry':enquiry,'sub':subs})
    else:
        return redirect('pc-view-submission')







@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def pc_select_supplier_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        s_id = request.POST.get('s_id', '0')
        r_id = request.POST.get('r_id', '0')
        just = request.POST.get('justification', '')

        enquiry=models.Request.objects.get(id=r_id)
        enquiry.job_open="No"
        enquiry.supplier_justification = just
        enquiry.assessement_id = s_id

        subs= models.Assessments.objects.get(id = s_id)

        enquiry.mechanic=subs.mechanic
        enquiry.save()
        # m= 'Good day '+ subs.mechanic+ ",\nplease note that you have been granted permission to work on \n JD : "+enquiry.problem_description+"\n Reg : "+enquiry.vehicle_reg
        # send_notice(m)
        return redirect('pc-view-submission')
        #return render(request,'vehicle/pc_view_submission.html',{'customer':customer,'enquiry':enquiry,'subs':subs})
    else:
        return JsonResponse({'response':'No get response'})





@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def pc_select_submissions_view1(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    if request.method=='POST':
        _id = request.POST.get('id', '0')
        enquiry=models.Request.objects.get(id=_id)
        subs= models.Assessments.objects.all().filter(job = enquiry.id)



        return render(request,'vehicle/pc_open_submission.html',{'customer':customer,'enquiry':enquiry,'subs':subs})
    else:
        return JsonResponse({'response':'No get response'})











@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_delete_request_view(request,pk):

    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=models.Request.objects.get(id=pk)
    enquiry.delete()
    return redirect('customer-view-request')

@login_required(login_url='customerlogin')
@user_passes_test(is_manager)
def customer_view_approved_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)


    enqs = []

    enquiries=models.Request.objects.all().filter( Q( Q(lab_manager=request.user.username)))
    services = models.Service.objects.all().filter(~Q(POP_date = '.'))
    servs = [x.request_id for x in services ]
    print('servs',servs)
    for enquiry in enquiries:
        #print('id',enquiry.id)
        if str(enquiry.id) in servs:
            enqs.append(enquiry)

            





    print('comparing ', customer.user.username)
    print('with', enquiries)


    return render(request,'vehicle/customer_view_request.html',{'customer':customer,'enquiries':enqs})




@login_required(login_url='customerlogin')
@user_passes_test(is_manager)
def customer_add_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=forms.RequestForm()
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        if enquiry.is_valid():
            enquiry_x=enquiry.save(commit=False)
            #customer=models.Customer.objects.get(pc=enquiry_x.user_id)

            # enquiry_x.pc=customer.user.username
            enquiry_x.customer1=enquiry_x.lab_manager
            enquiry_x.customer=enquiry_x.pc
            enquiry_x.save()
        else:
            print("form is invalid",enquiry.errors.as_data())
        return HttpResponseRedirect('customer-dashboard')
    return render(request,'vehicle/customer_add_request.html',{'enquiry':enquiry,'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/customer_profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm,'customer':customer}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('customer-profile')
    return render(request,'vehicle/edit_customer_profile.html',context=mydict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'vehicle/customer_invoice.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_feedback_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'vehicle/feedback_sent_by_customer.html',{'customer':customer})
    return render(request,'vehicle/customer_feedback.html',{'feedback':feedback,'customer':customer})
#============================================================================================
# CUSTOMER RELATED views END
#============================================================================================






#============================================================================================
# MECHANIC RELATED views start
#============================================================================================


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_dashboard_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    work_in_progress=models.Request.objects.all().filter(mechanic_id=mechanic.id,status='Repairing').count()
    work_completed=models.Request.objects.all().filter(mechanic_id=mechanic.id,status='Repairing Done').count()
    new_work_assigned=models.Request.objects.all().filter(mechanic_id=mechanic.id,status='Approved').count()
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_work_assigned':new_work_assigned,
    'salary':mechanic.salary,
    'mechanic':mechanic,
    }
    return render(request,'vehicle/mechanic_dashboard.html',context=dict)

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_work_assigned_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    works=models.Request.objects.all().filter(mechanic_id=mechanic.id)
    return render(request,'vehicle/mechanic_work_assigned.html',{'works':works,'mechanic':mechanic})


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_update_status_view(request,pk):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    updateStatus=forms.MechanicUpdateStatusForm()
    if request.method=='POST':
        updateStatus=forms.MechanicUpdateStatusForm(request.POST)
        if updateStatus.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.status=updateStatus.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/mechanic-work-assigned')
    return render(request,'vehicle/mechanic_update_status.html',{'updateStatus':updateStatus,'mechanic':mechanic})

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_attendance_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    attendaces=models.Attendance.objects.all().filter(mechanic=mechanic)
    return render(request,'vehicle/mechanic_view_attendance.html',{'attendaces':attendaces,'mechanic':mechanic})





@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_feedback_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'vehicle/feedback_sent.html',{'mechanic':mechanic})
    return render(request,'vehicle/mechanic_feedback.html',{'feedback':feedback,'mechanic':mechanic})

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_salary_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    workdone=models.Request.objects.all().filter(mechanic_id=mechanic.id).filter(Q(status="Repairing Done") | Q(status="Released"))
    return render(request,'vehicle/mechanic_salary.html',{'workdone':workdone,'mechanic':mechanic})

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_profile_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    return render(request,'vehicle/mechanic_profile.html',{'mechanic':mechanic})

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def edit_mechanic_profile_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=mechanic.user_id)
    userForm=forms.MechanicUserForm(instance=user)
    mechanicForm=forms.MechanicForm(request.FILES,instance=mechanic)
    mydict={'userForm':userForm,'mechanicForm':mechanicForm,'mechanic':mechanic}
    if request.method=='POST':
        userForm=forms.MechanicUserForm(request.POST,instance=user)
        mechanicForm=forms.MechanicForm(request.POST,request.FILES,instance=mechanic)
        if userForm.is_valid() and mechanicForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mechanicForm.save()
            return redirect('mechanic-profile')
    return render(request,'vehicle/edit_mechanic_profile.html',context=mydict)






#============================================================================================
# MECHANIC RELATED views start
#============================================================================================




# for aboutus and contact
def aboutus_view(request):
    return render(request,'vehicle/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'vehicle/contactussuccess.html')
    return render(request, 'vehicle/contactus.html', {'form':sub})



#***********************************send mail*****************************************
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
def send_notice(m="",):
    runya = 'takawengwa@brti.co.zw'

    message= m

    # send_mail(
    #     subject='TimeSheets Pending Approval',
    #     message=message,
    #     from_email=settings.EMAIL_HOST_USER,
    #     recipient_list=[emails[0],emails[1]]
    #     )

    for i in range(2):
        mimemsg = MIMEMultipart()
        mimemsg['From']="timesheet@brti.co.zw"
        mimemsg['To']='takaengwa@gmail.com'
        mimemsg['Cc']=runya
        mimemsg['Subject']="BRTI TimeSheets Pending Approval "
        mimemsg.attach(MIMEText(message, 'plain'))

                # with open(mail_attachment, "rb") as attachment:
                #     mimefile = MIMEBase('application', 'octet-stream')
                #     #mimefile.set_payload((attachment).read())
                # #     encoders.encode_base64(mimefile)
                # #     mimefile.add_header('Content-Disposition', "attachment; filename= %s" % mail_attachment_name)
                #     #mimemsg.attach(mimefile)
        connection = smtplib.SMTP(host='smtp.office365.com', port=587)
        connection.starttls()
        connection.login('timesheet@brti.co.zw','p@s3w0rd?1995')
        connection.send_message(mimemsg)
        connection.quit()








@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def reports_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all()



    return render(request,'vehicle/view_report.html',{'customer':customer,'enquiries':enquiries})




@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def get_table_data(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    dict_s= {}

    dict_r= {}
    if request.method=='POST':
       

        #enquiry.mechanic=subs.mechanic
        #enquiry.save()
  
        return JsonResponse({'response':'no data'})

    else:

        name = request.GET.get('name', '0')
        if name == 'req_completed': 
            enquiry=models.Service.objects.all().filter(~Q(POP_date="."))
            for enq in enquiry:
                dict_r[enq.id] = model_to_dict(models.Request.objects.get(id=enq.request_id)) | model_to_dict(enq)
            

        elif name == 'all_req':
            dict_r = {obj.pk: model_to_dict(obj) for obj in models.Request.objects.all()}

        elif name == 'all_bikes':
            dict_r = {obj.pk: model_to_dict(obj) for obj in models.Request.objects.all()}

        elif name == 'all_req':
            dict_r = {obj.pk: model_to_dict(obj) for obj in models.Request.objects.all()}





        #json_data = serializers.serialize('json', [models.Request.objects.get(id=enq.request_id)])

        return JsonResponse({'response':'success','data':dict_r})




import pandas as pd
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def post_rider_data(request):
    #df = pd.read_csv('vehicle\Book1.csv')
    
    for index, row in df.iterrows():
        print(f"Index: {index}, Name: {row['reg_num']}, Age: {row['age']}")


        bike = models.Bike()
        bike.reg_num = row['reg_num']
        bike.District = row['District']
        bike.Province= row['Province']
        bike.status = row['status']
        bike.status_date = row['status_date']
        bike.yr_procured = row['yr_procured']
        bike.reasons_for_non_f = row['reasons_for_non_f']
        bike.days_of_non_f = row['days_of_non_f']
        bike.age = row['age']
        bike.save()




