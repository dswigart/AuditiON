from django import forms

from AuditiON.constants import INSTRUMENT_LIST, AVAILABILITY_LIST, STATUS_CHOICES, CONFIRMATION_CHOICES, ADD_IGNORE

class ApplicantInfo(forms.Form):
    """ Data for superuser to filter applicant database query """
    instrument = forms.ChoiceField(label='instrument', choices=ADD_IGNORE(INSTRUMENT_LIST))
    status = forms.ChoiceField(label='status', choices=ADD_IGNORE(STATUS_CHOICES))
    confirmation = forms.ChoiceField(label='confirmation', choices=ADD_IGNORE(CONFIRMATION_CHOICES))
    availability = forms.ChoiceField(label='availability', choices=ADD_IGNORE(AVAILABILITY_LIST))
