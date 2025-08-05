"""
vehicle
"""
from django.contrib import admin
from django.urls import path
from vehicle import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.home_view,name=''),

    path('adminclick', views.adminclick_view),
    path('customerclick', views.customerclick_view),
    path('financeclick', views.financeclick_view),

    path('pcclick', views.pcclick_view),
    path('pcclick', views.pcclick_view),
    path('technicalclick', views.technicalclick_view),

    path('mechanicsclick', views.mechanicsclick_view),


    path('customerlogin', LoginView.as_view(template_name='vehicle/customerlogin.html'),name='customerlogin'),
    path('mechaniclogin', LoginView.as_view(template_name='vehicle/mechaniclogin.html'),name='mechaniclogin'),
    path('adminlogin', LoginView.as_view(template_name='vehicle/adminlogin.html'),name='adminlogin'),
    path('pclogin', LoginView.as_view(template_name='vehicle/adminlogin.html'),name='adminlogin'),
    path('technicallogin', LoginView.as_view(template_name='vehicle/adminlogin.html'),name='adminlogin'),
    path('financelogin', LoginView.as_view(template_name='vehicle/adminlogin.html'),name='adminlogin'),



    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),




    path('mechanic-dashboard', views.mechanic_dashboard_view,name='mechanic-dashboard'),
    path('mechanic-work-assigned', views.mechanic_work_assigned_view,name='mechanic-work-assigned'),
    path('mechanic-update-status/<int:pk>', views.mechanic_update_status_view,name='mechanic-update-status'),
    path('mechanic-feedback', views.mechanic_feedback_view,name='mechanic-feedback'),
    path('mechanic-salary', views.mechanic_salary_view,name='mechanic-salary'),
    path('mechanic-profile', views.mechanic_profile_view,name='mechanic-profile'),
    path('edit-mechanic-profile', views.edit_mechanic_profile_view,name='edit-mechanic-profile'),

    path('mechanic-attendance', views.mechanic_attendance_view,name='mechanic-attendance'),



    path('customer-dashboard', views.customer_dashboard_view,name='customer-dashboard'),
    path('customer-request', views.customer_request_view,name='customer-request'),
    path('customer-add-request',views.customer_add_request_view,name='customer-add-request'),

    path('customer-profile', views.customer_profile_view,name='customer-profile'),
    path('edit-customer-profile', views.edit_customer_profile_view,name='edit-customer-profile'),
    path('customer-feedback', views.customer_feedback_view,name='customer-feedback'),
    path('customer-invoice', views.customer_invoice_view,name='customer-invoice'),
    path('customer-view-request',views.customer_view_request_view,name='customer-view-request'),
    path('get_table_data',views.get_table_data,name='get_table_data'),


    path('post_rider_data',views.post_rider_data,name='post_rider_data'),

    path('pc-view-submission',views.pc_view_submissions_view,name='pc-view-submission'),
    path('pc-open-submission',views.pc_open_submissions_view,name='pc-open-submission'),
    path('pc-select-supplier',views.pc_select_supplier_view,name='pc-select-supplier'),
    path('pc-justify-supplier',views.pc_justify_supplier_view,name='pc-justify-supplier'),

    path('pc-view-approved-request',views.pc_view_approved_request_view,name='pc-view-approved-request'),
    path('pc-view-rejected-request',views.pc_view_rejected_request_view,name='pc-view-rejected-request'),
    path('pc-view-completed-request',views.pc_view_completed_request_view,name='pc-view-completed-request'),

    path('pc-view-request',views.pc_view_request_view,name='pc-view-request'),

    path('pc-open-request',views.pc_open_request_view,name='pc-open-request'),
    path('pc-approves-request',views.pc_approves_request_view,name='pc-approves-request'),
    
    path('view-reports',views.reports_view,name='view-reports'),

    path('tech-view-request',views.tech_view_request_view,name='tech-view-request'),
    path('tech-open-request',views.tech_open_request_view,name='tech-open-request'),
    path('tech-approves-request',views.tech_approves_request_view,name='tech-select-supplier'),

    path('tech-request',views.tech_request_view,name='tech-request'),
    path('tech-view-approved-request',views.tech_approved_request_view,name='tech-view-approved-request'),
    path('tech-view-rejected-request',views.tech_rejected_request_view,name='tech-view-rejected-request'),
    path('tech-view-pending-request',views.tech_pending_request_view,name='tech-view-pending-request'),


    path('tech-view-service',views.tech_view_services_view,name='tech-view-service'),
    path('tech-open-service',views.tech_open_service_view,name='tech-open-service'),
    path('tech-approves-service',views.tech_approves_service_view,name='tech-approves-service'),



    path('supplier-view-request',views.supplier_view_request_view,name='supplier-view-request'),
    path('supplier-open-request',views.supplier_open_request_view,name='supplier-open-request'),
    path('supplier-submits-request',views.supplier_submits_request_view,name='supplier-submits-request'),


    path('pending-awards',views.pending_awards,name='pending-awards'),
    path('current-awards',views.current_awards,name='current-awards'),
    path('past-awards',views.past_awards,name='past-awards'),

    path('view-awards',views.supplier_awards_view,name='view-awards'),
    path('update-award',views.supplier_update_award_view,name='update-award'),
    path('close-award',views.supplier_close_award_view,name='close-award'),
    path('send-record',views.send_record,name='send_record'),



    path('supplier-open-pending-award',views.supplier_open_pending_award,name='supplier-open-pending-award'),
    path('supplier-open-current-award',views.supplier_open_current_award,name='supplier-open-current-award'),
    path('supplier-open-past-award',views.supplier_open_past_award,name='supplier-open-past-award'),


    path('finance-view-request',views.finance_view_request_view,name='finance-view-request'),
    path('finance-open-request',views.finance_open_request_view,name='finance-open-request'),
    path('finance-approves-request',views.finance_approves_request_view,name='finance-approves-request'),


    path('finance-view-rejected-request',views.finance_view_rejected_request_view,name='finance-view-rejected-request'),
    path('finance-view-approved-request',views.finance_view_approved_request_view,name='finance-view-approved-request'),

    path('lo-request',views.lo_request_view,name='lo-request'),
    path('lo-uploads-pop',views.lo_uploads_pop_view,name='lo-uploads-pop'),


    
    path('lo-view-completed',views.lo_view_completed_request_view,name='lo-view-completed'),

    path('lo-view-jobs',views.lo_view_jobs_view,name='lo-view-jobs'),
    path('lo-open-job',views.lo_open_job_view,name='lo-open-job'),

    path('pc-view-jobs',views.pc_view_jobs_view,name='pc-view-jobs'),
    path('pc-open-job',views.pc_open_job_view,name='pc-open-job'),

    path('pc-approve-jobs',views.pc_justify_supplier_view,name='pc-justify-supplier'),
    path('pc-disapprove-jobs',views.pc_justify_supplier_view,name='pc-justify-supplier'),


    path('manager-view-jobs',views.manager_view_jobs_view,name='manager-view-jobs'),
    path('manager-open-job',views.manager_open_job_view,name='manager-open-job'),

    path('manager-approves-job',views.manager_approves_job_view,name='manager-approves-job'),


    path('pc-request',views.pc_request_view,name='pc-request'),
    path('finance-request',views.finance_request_view,name='finance-request'),
    path('manager-request',views.manager_request_view,name='manager-request'),





    path('customer-delete-request/<int:pk>', views.customer_delete_request_view,name='customer-delete-request'),
    path('customer-view-approved-request',views.customer_view_approved_request_view,name='customer-view-approved-request'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='vehicle/index.html'),name='logout'),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('pdf_view',views.pdf_view,name='pdf_view'),

    
]
