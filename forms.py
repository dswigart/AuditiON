from django import forms

from django.contrib.auth.models import User

from AuditiON.models import Instruments
from AuditiON.constants import AVAILABILITY_LIST, STATUS_CHOICES, CONFIRMATION_CHOICES, ADD_IGNORE, LOCK
from AuditiON.functions import get_judge_list, get_instrument_list, get_applicant_list, get_principal_list, get_judge_ins_list


class Locks(forms.Form):

    applicant_form_lock = forms.ChoiceField(label='Applicant Form Lock', choices=LOCK)
    judge_submission_form_lock = forms.ChoiceField(label='Judge Submission Form Lock', choices=LOCK)


class ApplicantInfo(forms.Form):
    """ Data for superuser to filter applicant database query """
    
    ###add an init!!!
    instrument = forms.ChoiceField(label='instrument', choices=ADD_IGNORE(get_instrument_list()))
    status = forms.ChoiceField(label='status', choices=ADD_IGNORE(STATUS_CHOICES))
    confirmation = forms.ChoiceField(label='confirmation', choices=ADD_IGNORE(CONFIRMATION_CHOICES))
    availability = forms.ChoiceField(label='availability', choices=ADD_IGNORE(AVAILABILITY_LIST))


class CreateJudge(forms.Form):
    """ Admin form to create judges """
    # note that there is a unique constraint on username. hack:'UniqueUser' in models.py
    username = forms.CharField(label='Username', max_length=20, help_text='best practice is to use firstlast ex: sarahviens')
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(label='Password', min_length=8, max_length=20, help_text='must be at least 8 characters')


class DeleteJudge(forms.Form):
    """ Admin form to delete judges """
    
    def __init__(self, *args, **kwargs):
        super(DeleteJudge, self).__init__(*args, **kwargs)
        self.fields['judges'].choices = get_judge_list()

    judges = forms.ChoiceField(label='Judges', choices=get_judge_list())


class ChangeJudgeEmail(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ChangeJudgeEmail, self).__init__(*args, **kwargs)
        self.fields['username'].choices = get_judge_list()
    
    username = forms.ChoiceField(label='Username', choices=get_judge_list())
    email = forms.EmailField(label='New Email Address')


class ChangeJudgePassword(forms.Form):

    username = forms.ChoiceField(label='Username', choices=get_judge_list())
    password = forms.CharField(label='New Password', min_length=8)


class AssociateJudge(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AssociateJudge, self).__init__(*args, **kwargs)
        self.fields['username'].choices = get_judge_list()
        self.fields['instrument'].choices = get_instrument_list()
    
    username = forms.ChoiceField(label='Judge', choices=get_judge_list())
    instrument = forms.ChoiceField(label='Instrument', choices=get_instrument_list())


class DeleteApplicant(forms.Form):

    def __init__(self, *args, **kwargs):
        super(DeleteApplicant, self).__init__(*args, **kwargs)
        self.fields['full_name'].choices = get_applicant_list()
    
    full_name = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=get_applicant_list())


class SelectApplicant(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SelectApplicant, self).__init__(*args, **kwargs)
        self.fields['applicant'].choices = get_applicant_list()
    
    applicant = forms.ChoiceField(label='Applicant', choices=get_applicant_list())


class DeletePrincipal(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(DeletePrincipal, self).__init__(*args, **kwargs)
        self.fields['full_name'].choices = get_principal_list()
    
    full_name = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=get_principal_list())


class SelectPrincipal(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(SelectPrincipal, self).__init__(*args, **kwargs)
        self.fields['principal'].choices = get_principal_list()
    
    principal = forms.ChoiceField(label='Principal', choices=get_principal_list())


class DeleteInstrument(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(DeleteInstrument, self).__init__(*args, **kwargs)
        self.fields['name'].choices = get_instrument_list()
    
    name = forms.ChoiceField(label='Instrument', choices=get_instrument_list())


class ToggleInstrument(forms.Form):
    def __init__(self, *args, **kwargs):
        judge = kwargs.pop('judge')
        super(ToggleInstrument, self).__init__(*args, **kwargs)
        self.fields['instrument_list'].choices = get_judge_ins_list(judge)
    
    instrument_list = forms.ChoiceField(label='Instrument_List')


