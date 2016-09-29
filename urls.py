from django.conf.urls import url

from . import views

urlpatterns = [
               
    # Applicants
    url(r'^$', views.index, name='index'),
    url(r'^audition_form$', views.audition_form, name='audition_form'),
    url(r'^audition_form_confirmation$', views.audition_form_confirmation,
        name='audition_form_confirmation'),
    url(r'^applicant_confirmation', views.applicant_confirmation,
        name='applicant_confirmation'),
               
    # Judges
    url(r'^judge_login$', views.judge_login, name='judge_login'),
    url(r'^judge_logout$', views.judge_logout, name='judge_logout'),
    url(r'^applicant_list$', views.applicant_list, name='applicant_list'),
    url(r'^applicant_selection$', views.applicant_selection,
        name='applicant_selection'),
               
    # General
    url(r'^form_success$', views.form_success, name='form_success'),
    url(r'^audition_closed$', views.audition_closed, name='audition_closed'),
    url(r'^database_problem$', views.database_problem, name='database_problem'),
    url(r'^access_denied$', views.access_denied, name='access_denied'),
    url(r'^already_confirmed$', views.already_confirmed, name='already_confirmed'),
               
    #------------------------------------------------------------------------#
    # Admin urls
               
    url(r'^on_admin_login$', views.on_admin_login, name='on_admin_login'),
    url(r'^on_admin_logout$', views.on_admin_logout, name='on_admin_logout'),
    url(r'^on_admin_home$', views.on_admin_home, name='on_admin_home'),
    url(r'^on_admin_db_info$', views.on_admin_db_info, name='on_admin_db_info'),
    url(r'^on_admin_data$', views.on_admin_data, name='on_admin_data'),
               
]
