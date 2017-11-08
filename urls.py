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
    url(r'^on_admin_accepted_confirmed$', views.on_admin_accepted_confirmed, name='on_admin_accepted_confirmed'),

    # Judges
    url(r'^on_admin_judge_home$', views.on_admin_judge_home, name='on_admin_judge_home'),
    url(r'^on_admin_create_judge$', views.on_admin_create_judge, name='on_admin_create_judge'),
    url(r'^on_admin_delete_judge$', views.on_admin_delete_judge, name='on_admin_delete_judge'),
    url(r'^on_admin_change_judge_email$', views.on_admin_change_judge_email, name='on_admin_change_judge_email'),
    url(r'^on_admin_change_judge_password$', views.on_admin_change_judge_password, name='on_admin_change_judge_password'),
    url(r'^on_admin_associate_judge$', views.on_admin_associate_judge, name='on_admin_associate_judge'),
    url(r'^on_admin_disassociate_judge$', views.on_admin_disassociate_judge, name='on_admin_disassociate_judge'),

    # Instruments
    url(r'^on_admin_instrument_home$', views.on_admin_instrument_home, name='on_admin_instrument_home'),
    url(r'^on_admin_create_instrument$', views.on_admin_create_instrument, name='on_admin_create_instrument'),
    url(r'^on_admin_delete_instrument$', views.on_admin_delete_instrument, name='on_admin_delete_instrument'),
    url(r'^on_admin_edit_score_order$', views.on_admin_edit_score_order, name='on_admin_edit_score_order'),

    # Locks
    url(r'^on_admin_locks$', views.on_admin_locks, name='on_admin_locks'),

    # data output
    url(r'^json_results$', views.json_results, name='json_results'),

    # Email
    url(r'^on_admin_email_home$', views.on_admin_email_home, name='on_admin_email_home'),
    url(r'^on_admin_email_accepted$', views.on_admin_email_accepted, name='on_admin_email_accepted'),
    url(r'^on_admin_email_accepted_test$', views.on_admin_email_accepted_test, name='on_admin_email_accepted_test'),

    # Applicants
    url(r'^on_admin_applicant_home$', views.on_admin_applicant_home, name='on_admin_applicant_home'),
    url(r'^on_admin_create_applicant$', views.on_admin_create_applicant, name='on_admin_create_applicant'),
    url(r'^on_admin_delete_applicant$', views.on_admin_delete_applicant, name='on_admin_delete_applicant'),
    url(r'^on_admin_edit_applicant_select$', views.on_admin_edit_applicant_select, name='on_admin_edit_applicant_select'),
    url(r'^on_admin_edit_applicant$', views.on_admin_edit_applicant, name='on_admin_edit_applicant'),

    # Principal
    url(r'^on_admin_principals_home$', views.on_admin_principals_home, name='on_admin_principals_home'),
    url(r'^on_admin_create_principal$', views.on_admin_create_principal, name='on_admin_create_principal'),
    url(r'^on_admin_delete_principal$', views.on_admin_delete_principal, name='on_admin_delete_principal'),
    url(r'^on_admin_edit_principal_select$', views.on_admin_edit_principal_select, name='on_admin_edit_principal_select'),
    url(r'^on_admin_edit_principal$', views.on_admin_edit_principal, name='on_admin_edit_principal'),
    # Productions
    url(r'^on_admin_production_data_home$', views.on_admin_production_data_home, name='on_admin_production_data_home'),
]
