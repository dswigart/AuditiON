
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.forms import modelformset_factory, modelform_factory
from django.db import Error, connection
from django.core.exceptions import ObjectDoesNotExist

from .models import Applicant, ApplicantForm, AuditionControl


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
            return render(request, 'AuditiON/form_confirmation.html',
                         {'form':form})

    # first time through, render empty form if audition is open
    else:
        form = ApplicantForm()
    return render(request, 'AuditiON/form.html', {'form':form})


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
            form.save()
            return HttpResponseRedirect(reverse('form_success'))
        else:
            return render(request, 'AuditiON/form.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('access_denied'))

def applicant_confirmation(request):
    """ Accepted applicants confirm or reject their invitation """
    if (request.method == 'GET'):
        if 'code' in request.GET:
            Appform = modelform_factory(Applicant, fields=('first_name',
                                                              'confirmation', 'code'))
            try:
                x = Applicant.objects.get(code=request.GET['code'])
            except ObjectDoesNotExist:
                return HttpResponseRedirect(reverse('database_problem'))
            if (x.confirmation == 'Unconfirmed'):
                form = Appform(instance=x)
                return render(request, 'AuditiON/applicant_confirmation.html',
                              {'form':form})
            else:
                #create confirmed page with reached this in error contact admin message
                return HttpResponse('FIX THIS')
        else:
            return HttpResponseRedirect('access_denied')

    elif (request.method == 'POST'):
        Appform = modelform_factory(Applicant, fields=('first_name',
                                                          'confirmation', 'code'))
        form = Appform(request.POST)
        if form.is_valid():
            # modelform is executing an INSERT instead of an UPDATE. Unable to
            # determine why--dropped down to raw sql.
            cursor = connection.cursor()
            cursor.execute('UPDATE AuditiON_Applicant SET confirmation = %s WHERE code = %s', [form['confirmation'].data, form['code'].data])
            
            return HttpResponseRedirect('form_success')
        else:
            return render(request, 'applicant_confirmation', {'form':form})

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
        # looking up all applicants whose instrument matches username
        instrument = request.user.username
        try:
            applicant_list = Applicant.objects.filter(instrument__exact=instrument)
        except (ObjectDoesNotExist):
            return HttpResponseRedirect(reverse('database_problem'))
        
        return render(request, 'AuditiON/applicant_list.html', {'applicant_list':applicant_list})
    else:
        return HttpResponseRedirect(reverse('access_denied'))


# applicant_list redirects here when judge clicks on 'select
# applicants' link on applicant_list page
def applicant_selection(request):
    """ Displays applicants by instrument for selection (edit 'status' in db) """
    # set-up to check if judge submission is open or closed
    try:
        controls = AuditionControl.objects.get(reference_name='controls')
    except (ObjectDoesNotExist):
        return HttpResponseRedirect(reverse('database_problem'))
    lock = controls.judge_submission_form_lock
    
    # redirect if closed
    if (lock == 'Locked'):
        return HttpResponseRedirect(reverse('access_denied'))

    if request.user.is_active:
        if (request.POST):
            ApplicantFormSet = modelformset_factory(Applicant, fields=('first_name', 'last_name', 'status',), extra=0)
            set = ApplicantFormSet(request.POST)
            if (set.is_valid):
                set.save()
                return HttpResponseRedirect(reverse('form_success'))
            else:
                return HttpResponseRedirect(reverse('database_problem'))
        else:
            # looking up all applicants whose instrument matches username
            instrument = request.user.username
            
            # building formset
            ApplicantFormSet = modelformset_factory(Applicant, fields=('first_name', 'last_name', 'status', 'part'), extra=0)
            set = ApplicantFormSet(queryset=Applicant.objects.filter(
                instrument__exact=instrument))
            return render(request, 'AuditiON/applicant_selection.html', {'set':set})
    else:
        return HttpResponseRedirect(reverse('access_denied'))


def form_success(request):
    return render(request, 'AuditiON/success.html')


# 2 redirects here for different reasons, make notes!
def audition_closed(request):
    return render(request, 'AuditiON/audition_closed.html')


def database_problem(request):
    return render(request, 'AuditiON/database_problem.html')

def access_denied(request):
    return render(request, 'AuditiON/access_denied.html')




