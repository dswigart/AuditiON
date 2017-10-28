import uuid
import csv

from datetime import datetime

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms import modelformset_factory, modelform_factory
from django.db import Error, connection
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from AuditiON.models import Applicant, ApplicantForm, CreateInstrument, AuditionControl, Instruments, ApplicantEditForm, Principal, CreatePrincipal, PrincipalEditForm, ProductionData, ProductionDataForm, StockEmailData, StockEmailDataForm
from AuditiON.forms import ApplicantInfo, CreateJudge, DeleteJudge, DeleteInstrument, ChangeJudgeEmail, ChangeJudgePassword, AssociateJudge, Locks, DeleteApplicant, SelectApplicant, DeletePrincipal, SelectPrincipal, ToggleInstrument
import AuditiON.functions as functions
import AuditiON.EmailHelper as EmailHelper

def index(request):
    return HttpResponseRedirect(reverse('audition_form'))


def audition_form(request):
    """ A form for applicants' information """
    # set-up to check if audition is open or closed
    try:
        controls = AuditionControl.objects.get(reference_name='controls')
    except (ObjectDoesNotExist):
        return HttpResponseRedirect(reverse('database_problem'))
    lock = controls.applicant_form_lock

    # redirect if audition is closed
    if (lock == 'Locked'):
        return HttpResponseRedirect(reverse('audition_closed'))

    # render confirmation page if form data is valid
    if (request.method == 'POST'):
        form = ApplicantForm(request.POST)
        if form.is_valid():
            x = functions.youtube_split(form.cleaned_data['youtube_link'])
            return render(request, 'AuditiON/form_confirmation.html',
                         {'form':form, 'youtube_string': x})
        else:
            production_data = ProductionData.objects.get(name='production_data')
            return render(request, 'AuditiON/form.html', {'form':form,'production_data':production_data})
    # first time through, render empty form if audition is open
    else:
        form = ApplicantForm()
        production_data = ProductionData.objects.get(name='production_data')

    return render(request, 'AuditiON/form.html', {'form':form,'production_data':production_data})


def audition_form_confirmation(request):
    """ Validates data from audition_form then saves or returns errors """
    # set-up to check if audition is open or closed
    try:
        controls = AuditionControl.objects.get(reference_name='controls')
    except (ObjectDoesNotExist):
        return HttpResponseRedirect(reverse('database_problem'))
    lock = controls.applicant_form_lock

    # redirect if audition is closed
    if (lock == 'Locked'):
        return HttpResponseRedirect(reverse('audition_closed'))

    # save valid form. form was already tested for validity in previous view,
    # if for any reason it is invalid, returns errors to audition_form
    if (request.method == 'POST'):
        form = ApplicantForm(request.POST)
        if form.is_valid():
            form.instance.youtube_link = functions.youtube_split(form.instance.youtube_link)
            form.instance.code = uuid.uuid4().hex
            form.save()
            try:
                send_mail('Application Submitted', '%s %s, %s' % (form.instance.first_name, form.instance.last_name, form.instance.instrument), 'orchestranext@gmail.com', ['orchestranext@gmail.com'], fail_silently=True,)
            except Exception:
                pass
            try:
                send_mail('Application Submitted', 'Dear %s,\n\nThis email confirmed that we have received your application for the 2017-18 season!\n\nYou will be notified of the results by email on Nov. 1. We wish you the very best of luck!\n\nCheers,\n\nOrchestra Next\nBrian McWhorter, music director\nSarah Viens, trumpet/artistic admin' % (form.instance.first_name, ), 'orchestranext@gmail.com', [form.instance.email_address], fail_silently=True,)
            except Exception:
                pass
            return HttpResponseRedirect('http://www.orchestranext.com/success')
        else:
            return render(request, 'AuditiON/form.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def applicant_confirmation(request):
    """ Accepted applicants confirm or reject their invitation """
    if (request.method == 'GET'):
        if 'code' in request.GET:
            Appform = modelform_factory(Applicant, fields=('first_name',
                                                              'confirmation', 'code', 'availability', 'avail_explain'))
            try:
                x = Applicant.objects.get(code=request.GET['code'])
            except ObjectDoesNotExist:
                return HttpResponseRedirect(reverse('database_problem'))
            if (x.confirmation == 'Unconfirmed'):
                form = Appform(instance=x)
                first_name = form.instance.first_name
                availability = form.instance.availability
                avail_explain = form.instance.avail_explain
                return render(request, 'AuditiON/applicant_confirmation.html',
                              {'form':form, 'first_name':first_name, 'availability':availability, 'avail_explain':avail_explain})
            else:
                return HttpResponseRedirect(reverse('already_confirmed'))
        else:
            return HttpResponseRedirect(reverse('access_denied'))

    elif (request.method == 'POST'):
        Appform = modelform_factory(Applicant, fields=('first_name',
                                                          'confirmation', 'code'))
        form = Appform(request.POST)
        if form.is_valid():
            # modelform is executing an INSERT instead of an UPDATE. Unable to
            # determine why--dropped down to raw sql.
            cursor = connection.cursor()
            cursor.execute('UPDATE "AuditiON_applicant" SET confirmation = %s WHERE code = %s', [form['confirmation'].data, form['code'].data])
            return HttpResponseRedirect('form_success')
        # the only reason for invalid form is tampering, deny access
        else:
            return HttpResponseRedirect(reverse('access_denied'))

    else:
        return HttpResponseRedirect(reverse('access_denied'))


def judge_login(request):
    """ Logs in Judges as Users """
    if (request.method == 'POST'):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('applicant_list'))
        else:
            return render(request, 'AuditiON/judge_login.html',
                          {'form':form, 'user':user})
    else:
        form = AuthenticationForm()
        return render(request, 'AuditiON/judge_login.html', {'form':form})


def judge_logout(request):
    """ Logs out Judges (Users) """
    logout(request)
    return HttpResponseRedirect(reverse('judge_login'))


# judge_login redirects here
def applicant_list(request):
    """ Displays applicants by instrument for judge evaluation """
    if request.user.is_active:

        if (request.method == 'GET'):
            instrument_list = ToggleInstrument(judge=request.user)
            return render(request, 'AuditiON/applicant_list.html', {'instrument_list':instrument_list})

        if (request.method == 'POST'):
            instrument = request.POST.get('instrument_list')
            instrument = Instruments.objects.get(name=instrument)
            instrument_list = ToggleInstrument(judge=request.user)
            try:
                applicant_list = Applicant.objects.filter(instrument__exact=instrument).order_by('last_name')
            except (ObjectDoesNotExist):
                return HttpResponseRedirect(reverse('database_problem'))
            applicant_count = applicant_list.count()
            return render(request, 'AuditiON/applicant_list.html', {'instrument_list':instrument_list,'instrument':instrument,'applicant_list':applicant_list, 'applicant_count':applicant_count})
    else:
        return HttpResponseRedirect(reverse('access_denied'))


# applicant_list redirects here when judge clicks on 'submit choices'
# link on applicant_list page
def applicant_selection(request):
    """ Displays applicants by instrument for selection (edit 'status' and 'ranking' in db) """
    # set-up to check if judge submission is open or closed
    try:
        controls = AuditionControl.objects.get(reference_name='controls')
    except (ObjectDoesNotExist):
        return HttpResponseRedirect(reverse('database_problem'))
    lock = controls.judge_submission_form_lock
    # redirect if closed
    if (lock == 'Locked'):
        return HttpResponseRedirect(reverse('access_denied'))

    if (request.user.is_active):
        if (request.method == 'GET'):
            if (request.GET.get('instrument_list')):
                instrument = request.GET.get('instrument_list')
                instrument = Instruments.objects.get(name=instrument)
                instrument_list = ToggleInstrument(judge=request.user)

                ApplicantFormSet = modelformset_factory(Applicant, fields=('first_name', 'last_name', 'status', 'ranking'), extra=0)
                set = ApplicantFormSet(queryset=Applicant.objects.filter(instrument__exact=instrument).order_by('last_name'))
                return render(request, 'AuditiON/applicant_selection.html', {'instrument':instrument, 'set':set, 'instrument_list':instrument_list})
            else:
                instrument_list = ToggleInstrument(judge=request.user)
                return render(request, 'AuditiON/applicant_selection.html', {'instrument_list':instrument_list})

        if (request.method == 'POST'):
            ApplicantFormSet = modelformset_factory(Applicant, fields=('first_name', 'last_name', 'status', 'ranking'), extra=0)
            set = ApplicantFormSet(request.POST)
            if (set.is_valid):
                set.save()
                return HttpResponseRedirect(reverse('applicant_list'))
            else:
                return HttpResponseRedirect(reverse('database_problem'))

    else:
        return HttpResponseRedirect(reverse('access_denied'))


def form_success(request):
    logout(request)
    return render(request, 'AuditiON/success.html')


def audition_closed(request):
    return render(request, 'AuditiON/audition_closed.html')


def database_problem(request):
    return render(request, 'AuditiON/database_problem.html')


def access_denied(request):
    return render(request, 'AuditiON/access_denied.html')


def already_confirmed(request):
    return render(request, 'AuditiON/already_confirmed.html')


# ----------------------------------------------------------- #
# Administration Views


def on_admin_login(request):
    """ Logs in Admin as User """
    if (request.method == 'POST'):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('on_admin_home'))
        else:
            return render(request, 'AuditiON/on_admin_login.html',
                          {'form':form, 'user':user})
    else:
        form = AuthenticationForm()
        return render(request, 'AuditiON/on_admin_login.html', {'form':form})


def on_admin_home(request):
    """ Admin home page """
    if (request.user.is_superuser):
        count = Applicant.objects.count()

        return render(request, 'AuditiON/on_admin_home.html', {'count':count})
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_db_info(request):
    """ Returns filtered applicants for display to superusers """
    if (request.user.is_superuser):
        if (request.method == 'GET'):
            form = ApplicantInfo()
            count = Applicant.objects.count()
            return render(request, 'AuditiON/on_admin_db_info.html', {'form':form, 'count':count})
        if (request.method == 'POST'):
            form = ApplicantInfo(request.POST)
            if form.is_valid():
                set = functions.get_filtered_db_info(form.cleaned_data)
                count = Applicant.objects.count()
                #later, put set in score order
                return render(request, 'AuditiON/on_admin_db_info.html', {'form':form, 'set':set, 'count':count})
            else:
                pass
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_locks(request):

    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            locks = AuditionControl.objects.get(reference_name='controls')
            form = Locks(initial={'applicant_form_lock':locks.applicant_form_lock, 'judge_submission_form_lock':locks.judge_submission_form_lock})
            return render(request, 'AuditiON/on_admin_locks.html', {'form':form })
        if (request.method == 'POST'):
            form = Locks(request.POST)
            if form.is_valid():
                locks = AuditionControl.objects.get(reference_name='controls')
                locks.applicant_form_lock = form.cleaned_data['applicant_form_lock']
                locks.judge_submission_form_lock = form.cleaned_data['judge_submission_form_lock']
                locks.save()
                return HttpResponseRedirect(reverse('on_admin_locks'))
            else:
                return render(request, 'AuditiON/on_admin_locks.html', {'form':form })

    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_judge_home(request):
    """ Admin home for judge data and control """
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            judges = User.objects.all()
            count = Applicant.objects.count()
            return render(request, 'AuditiON/on_admin_judge_home.html', {'judges':judges, 'count':count})

    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_create_judge(request):
    """ Create Judges """
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = CreateJudge()
            count = Applicant.objects.count()
            return render(request, 'AuditiON/on_admin_create_judge.html', {'form':form, 'count':count})
        if (request.method == 'POST'):
            form = CreateJudge(request.POST)
            if form.is_valid():
                # hack: 'UniqueUser'
                # action: must catch db error and provide custom notification
                try:
                    new_judge = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
                    new_judge.save()
                except (Error):
                    unique = True
                    return render(request, 'AuditiON/on_admin_create_judge.html', {'form':form, 'unique':unique})

                return HttpResponseRedirect(reverse('on_admin_judge_home'))
            else:
                return render(request, 'AuditiON/on_admin_create_judge.html', {'form':form})

    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_delete_judge(request):
    """ Delete judges """
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = DeleteJudge()
            return render(request, 'AuditiON/on_admin_delete_judge.html', {'form':form})
        if (request.method == 'POST'):
            post = request.POST.getlist('judges')
            for judge in post:
                name_match = User.objects.filter(username__exact=judge)
                for name in name_match:
                    # Superusers cannot delete each other or themselves
                    if not name.is_superuser:
                        name.delete()
            return HttpResponseRedirect(reverse('on_admin_judge_home'))
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_change_judge_email(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = ChangeJudgeEmail()
            return render(request, 'AuditiON/on_admin_change_judge_email.html', {'form':form})
        if (request.method == 'POST'):
            form = ChangeJudgeEmail(request.POST)
            if form.is_valid():
                judge = User.objects.get(username=form.cleaned_data['username'])
                # Superuser may not change another superuser's email
                if (request.user.username != judge.username and judge.is_superuser):
                    return HttpResponseRedirect(reverse('on_admin_judge_home'))
                judge.email = form.cleaned_data['email']
                judge.save()
                return HttpResponseRedirect(reverse('on_admin_judge_home'))
            else:
                return render(request, 'AuditiON/on_admin_change_judge_email.html', {'form':form})

    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_change_judge_password(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = ChangeJudgePassword()
            return render(request, 'AuditiON/on_admin_change_judge_password.html', {'form':form})
        if (request.method == 'POST'):
            form = ChangeJudgePassword(request.POST)
            if form.is_valid():
                judge = User.objects.get(username=form.cleaned_data['username'])
                # Superuser may not change another superuser's password
                if (request.user.username != judge.username and judge.is_superuser):
                    return HttpResponseRedirect(reverse('on_admin_judge_home'))
                judge.password = make_password(form.cleaned_data['password'])
                judge.save()
                return HttpResponseRedirect(reverse('on_admin_judge_home'))
            else:
                return render(request, 'AuditiON/on_admin_change_judge_password.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_instrument_home(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = Instruments.objects.all()
            return render(request, 'AuditiON/on_admin_instrument_home.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_create_instrument(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            instruments = Instruments.objects.all()
            form = CreateInstrument()
            return render(request, 'AuditiON/on_admin_create_instrument.html', {'form':form, 'instruments':instruments})
        if (request.method == 'POST'):
            form = CreateInstrument(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('on_admin_instrument_home'))

    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_delete_instrument(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            instruments = Instruments.objects.all()
            form = DeleteInstrument()
            return render(request, 'AuditiON/on_admin_delete_instrument.html', {'form':form, 'instruments':instruments})
        if (request.method == 'POST'):
            inst_name = request.POST.getlist('name')
            instrument = Instruments.objects.get(name=inst_name[0])
            instrument.delete()
            return HttpResponseRedirect(reverse('on_admin_instrument_home'))

    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_associate_judge(request):
    """ Associate judge with instrument """
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = AssociateJudge()
            return render(request, 'AuditiON/on_admin_associate_judge.html', {'form':form})
        if (request.method == 'POST'):
            form = AssociateJudge(request.POST)
            if form.is_valid():
                judge = User.objects.get(username=form.cleaned_data['username'])
                instrument = Instruments.objects.get(name=form.cleaned_data['instrument'])
                judge.ins.add(instrument)
                return HttpResponseRedirect(reverse('on_admin_judge_home'))
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_disassociate_judge(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET' and not request.GET.getlist('judges')):
            judge_form = DeleteJudge()
            return render(request, 'AuditiON/on_admin_disassociate_judge.html', {'judge_form':judge_form})
        if (request.method == 'GET' and request.GET.getlist('judges')):
            judge = request.GET.getlist('judges')
            judge_form2 = DeleteJudge(request.GET)
            judge = User.objects.get(username=judge[0])
            instrument_form = ToggleInstrument(judge=judge)
            return render(request, 'AuditiON/on_admin_disassociate_judge.html', {'instrument_form':instrument_form, 'judge_form2':judge_form2})
        if (request.method == 'POST'):
            judge = request.POST.getlist('judges')
            print judge
            print request.POST
            judge = User.objects.get(username=judge[0])
            instrument = request.POST.getlist('instrument_list')
            instrument = Instruments.objects.get(name=instrument[0])
            judge.ins.remove(instrument)
            return HttpResponseRedirect(reverse('on_admin_judge_home'))
    else:
        return HttpResponseRedirect(reverse('access_denied'))



def on_admin_applicant_home(request):
    """ Admin home for applicant data and control """
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            applicants = Applicant.objects.all()
            count = Applicant.objects.count()
            return render(request, 'AuditiON/on_admin_applicant_home.html', {'applicants':applicants, 'count':count})

    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_create_applicant(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = ApplicantForm()
            return render(request, 'AuditiON/on_admin_create_applicant.html', {'form':form})
        if (request.method == 'POST'):
            form = ApplicantForm(request.POST)
            if form.is_valid():
                form.instance.youtube_link = functions.youtube_split(form.instance.youtube_link)
                form.instance.code = uuid.uuid4().hex
                form.save()
                return HttpResponseRedirect(reverse('on_admin_applicant_home'))
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_delete_applicant(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = DeleteApplicant()
            return render(request, 'AuditiON/on_admin_delete_applicant.html', {'form':form})
        if (request.method == 'POST'):
            post = request.POST.getlist('full_name')
            for applicant in post:
                code_match = Applicant.objects.filter(code__exact=applicant)
                for name in code_match:
                    name.delete()
        return HttpResponseRedirect(reverse('on_admin_applicant_home'))
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_edit_applicant_select(request):
    """  for use with on_admin_edit_applicant """
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = SelectApplicant()
            return render(request, 'AuditiON/on_admin_edit_applicant_select.html', {'form':form})

    else:
        return HttpResponseRedirect(reverse('access_denied'))


# On_admin_edit_applicant_select routes here
# could be done in one page as in on_admin_disassociate_judge
def on_admin_edit_applicant(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            applicant_code = request.GET.getlist('applicant')
            applicant = Applicant.objects.get(code=applicant_code[0])
            form = ApplicantEditForm(instance=applicant)
            form.initial['youtube_link'] = 'www.youtu.be/%s' % (form.instance.youtube_link)
            return render(request, 'AuditiON/on_admin_edit_applicant.html', {'form':form})
        if (request.method == 'POST'):
            applicant = Applicant.objects.get(code=request.POST['code'])
            form = ApplicantEditForm(request.POST, instance=applicant)
            if form.is_valid():
                form.instance.youtube_link = functions.youtube_split(form.instance.youtube_link)
                form.save()
                return HttpResponseRedirect(reverse('on_admin_applicant_home'))
            else:
                return render(request, 'AuditiON/on_admin_edit_applicant.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_principals_home(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = Principal.objects.all()
            return render(request, 'AuditiON/on_admin_principals_home.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_create_principal(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = CreatePrincipal()
            return render(request, 'AuditiON/on_admin_create_principal.html', {'form':form})
        if (request.method == 'POST'):
            form = CreatePrincipal(request.POST)
            if form.is_valid():
                form.instance.code = uuid.uuid4().hex
                form.save()
                return HttpResponseRedirect(reverse('on_admin_principals_home'))
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_delete_principal(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = DeletePrincipal()
            return render(request, 'AuditiON/on_admin_delete_principal.html', {'form':form})
        # to be want to give the option to delete more than one principal at a time?
        # THIS IS WHERE YOU ARE
        if (request.method == 'POST'):
            post = request.POST.getlist('full_name')
            for principal in post:
                code_match = Principal.objects.filter(code__exact=principal)
                for name in code_match:
                    name.delete()
        return HttpResponseRedirect(reverse('on_admin_principals_home'))
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_edit_principal_select(request):
    """  for use with on_admin_edit_applicant """
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            form = SelectPrincipal()
            return render(request, 'AuditiON/on_admin_edit_principal_select.html', {'form':form})

    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_edit_principal(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            principal_code = request.GET.getlist('principal')
            principal = Principal.objects.get(code=principal_code[0])
            form = PrincipalEditForm(instance=principal)
            return render(request, 'AuditiON/on_admin_edit_principal.html', {'form':form})
        if (request.method == 'POST'):
            principal = Principal.objects.get(code=request.POST['code'])
            form = PrincipalEditForm(request.POST, instance=principal)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('on_admin_principals_home'))
            else:
                return render(request, 'AuditiON/on_admin_edit_principal.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_production_data_home(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            production_data = ProductionData.objects.get(name='production_data')
            form = ProductionDataForm(instance=production_data)
            return render(request, 'AuditiON/on_admin_production_data_home.html', {'form':form, 'production_data':production_data})
        if (request.method == 'POST'):
            form = ProductionDataForm(request.POST)
            cursor = connection.cursor()
            cursor.execute('UPDATE "AuditiON_productiondata" SET data = %s WHERE name = %s', [form['data'].data, form['name'].data])
            return HttpResponseRedirect(reverse('on_admin_production_data_home'))
        else:
            return render(request, 'AuditiON/on_admin_production_data_home.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_email_home(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            return render(request, 'AuditiON/on_admin_email_home.html')

    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_email_accepted(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        if (request.method == 'GET'):
            accepted_confirmation = StockEmailData.objects.get(email_name='accepted_confirmation')
            form = StockEmailDataForm(instance=accepted_confirmation)
            return render(request, 'AuditiON/on_admin_email_accepted.html', {'form':form})
        if (request.method == 'POST'):
            applicant_confirmation = StockEmailData.objects.get(email_name=request.POST['email_name'])
            form = StockEmailDataForm(request.POST, instance=applicant_confirmation)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('on_admin_email_accepted'))
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_email_accepted_test(request):
    if (request.user.is_superuser):
        if (functions.deny_brian(request.user.get_username())):
            return HttpResponseRedirect(reverse('access_denied'))

        # edit data down to few applicants
        applicants = Applicant.objects.filter(status__exact='Accepted')
        print type(applicants)
        applicants = applicants[0:2]
        print type(applicants)
        for applicant in applicants:
            # don't email the applicant with a test!!
            applicant.email_address = u'orchestranext@gmail.com'

        eh = EmailHelper.EmailHelper()
        messages = eh.accepted_applicant_conf(applicants)
        for message in messages:
            print message.recipients()
            try:
                print 'before send'
                message.send(fail_silently=True)
                print 'after send'
            except Exception as err:
                print err
        print 'before redirect'
        return HttpResponseRedirect(reverse('on_admin_email_accepted'))

    else:
        return HttpResponseRedirect(reverse('access_denied'))

def on_admin_data(request):
    """ Create CSV of all applicants for download """
    if (request.user.is_superuser):
        #Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ONdatabase.csv"'

        #all applicants in database
        data = Applicant.objects.all()

        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Phone Number', 'Email Address', 'Zip Code', 'Age', 'School', 'Instrument', 'Availability', 'Availability Explaination', 'Youtube Link', 'Ranking', 'Status', 'Confirmation',])
        for x in data:
            writer.writerow([x.first_name, x.last_name, x.phone_number, x.email_address, x.zip_code, x.age, x.school, x.instrument, x.availability, x.avail_explain, 'https://youtu.be/' +  x.youtube_link, x.ranking, x.status, x.confirmation,])
        return response
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def on_admin_accepted_confirmed(request):
    """ Create CSV of accepted/alternate applicants who have confirmed for download """
    if (request.user.is_superuser):
        #Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="accepted_alternate_confirmed.csv"'

        #filter accepted and alternates who have confirmed
        accepted = Applicant.objects.filter(status__contains='Accepted').filter(confirmation__exact='Accept')
        alternate = Applicant.objects.filter(status__contains='Alternate').filter(confirmation__exact='Accept')

        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Phone Number', 'Email Address', 'Zip Code', 'Age', 'School', 'Instrument', 'Availability', 'Availability Explaination', 'Youtube Link', 'Ranking', 'Status', 'Confirmation',])
        for x in accepted:
            writer.writerow([x.first_name, x.last_name, x.phone_number, x.email_address, x.zip_code, x.age, x.school, x.instrument, x.availability, x.avail_explain, 'https://youtu.be/' +  x.youtube_link, x.ranking, x.status, x.confirmation,])
        writer.writerow('\n')
        for x in alternate:
            writer.writerow([x.first_name, x.last_name, x.phone_number, x.email_address, x.zip_code, x.age, x.school, x.instrument, x.availability, x.avail_explain, 'https://youtu.be/' +  x.youtube_link, x.ranking, x.status, x.confirmation,])
        return response
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def json_results(request):
    accepted = Applicant.objects.filter(status__contains='Accepted').filter(confirmation__exact='Accept')
    alternate = Applicant.objects.filter(status__contains='Alternate').filter(confirmation__exact='Accept')

    results = {}
    for applicant in accepted:
        full_name = applicant.first_name + applicant.last_name
        if (applicant.instrument.name not in results):
            reference = [(applicant.instrument.name, [full_name])]
            results.update(reference)
            print 'in if block'
        else:
            reference = results[applicant.instrument.name]
            reference.append(full_name)
            print 'in else block'
    return JsonResponse(results)


def on_admin_logout(request):
    """ Logs out superusers """
    logout(request)
    return HttpResponseRedirect(reverse('on_admin_login'))
