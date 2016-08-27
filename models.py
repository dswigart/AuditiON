import uuid

from django.db import models
from django.forms import ModelForm
from django.core.validators import RegexValidator

from .constants import AVAILABILITY_LIST, CONFIRMATION_CHOICES, STATUS_CHOICES, INSTRUMENT_LIST, PART_CHOICES, LOCK

class Applicant(models.Model):
    """ Main data for Orchestra applicants """
    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    phone_number = models.CharField('Phone Number', max_length=17)
    email_address = models.EmailField('Email Address')
    zip_code = models.CharField('Zip Code', max_length=5)
    age = models.CharField('Age', max_length=3)
    school = models.CharField('School', max_length=40)
    instrument = models.CharField('Instrument', max_length=25,
                                    choices=INSTRUMENT_LIST)
    availability = models.CharField('Availability', max_length=6,
                                    choices=AVAILABILITY_LIST, help_text='Nutcracker: rehearsals on Dec 14 & 15, 7-10pm. Shows on Dec 16 7:30pm, Dec 17 2pm & 7:30pm, Dec 18 2pm. Midsummer Night\'s Dream (2017): rehearsals on Feb 7 7-10pm, Feb 8 7-10pm, Feb 9 7-10pm, Feb 10 7-10pm. Shows on Feb 11 7:30pm, Feb 12 2pm. Snow Queen (2017): rehearsals on Apr 4 7-10pm, Apr 5 7-10pm, Apr 6 7-10pm, Apr 7 7-10pm. Shows on Apr 8 7:30pm, Apr 9 2pm.')
    avail_explain = models.TextField('Availability Explaination',
                                     default='All', help_text='If \'some\' was marked above, please note rehearsals or shows you cannot attend and provide a brief explaination.')
    youtube_link = models.CharField('YouTube Link ID', max_length=20, default='ex. \'64T3yu7Sd\'', help_text='We only need the string that uniquely identify\'s your video. \'https://wwww.youtube.com/watch?v=\' OR \'https://youtu.be/\' should be left out.')
                            
    """validators=[RegexValidator('(www.)?youtu(be.com|.be)','Enter a valid YouTube link')])"""
    part = models.CharField(max_length=15, choices=PART_CHOICES, default='Unassigned')
    status = models.CharField(max_length=9, choices=STATUS_CHOICES,
                              default='Rejected')
    confirmation = models.CharField(max_length=12, choices=CONFIRMATION_CHOICES,
                                    default='Unconfirmed')
    code = models.CharField(max_length=40, default=uuid.uuid4().hex)
    submission_date_time = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        exclude = ['status', 'part', 'confirmation', 'code']


class AuditionControl(models.Model):
    """ Control panel for SuperUser """
    # note: reference_name must be set to 'controls'
    # note: only one row should exist in this model
    reference_name = models.CharField(max_length=9, primary_key=True)
    applicant_form_lock = models.CharField(max_length=8, choices=LOCK)
    judge_submission_form_lock = models.CharField(max_length=8, choices=LOCK)
    

    def __str__(self):
        return 'Applicant form is: %s and Judge submission form is: %s' % (self.applicant_form_lock, self.judge_submission_form_lock)


class StockEmailData(models.Model):
    """ Email content editable by SuperUser """
    email_name = models.CharField(max_length=100)
    subject_line = models.TextField()
    content_body = models.TextField()

    def __str__(self):
        return self.email_name


