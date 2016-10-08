
from django.db import models
from django.forms import ModelForm
from django.core.validators import RegexValidator

from .constants import AVAILABILITY_LIST, CONFIRMATION_CHOICES, STATUS_CHOICES, INSTRUMENT_LIST, RANKING_CHOICES, LOCK

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
                                    choices=AVAILABILITY_LIST)
    avail_explain = models.TextField('Availability Explaination',
                                     default='All', help_text='If \'some\' was marked above, please note rehearsals or shows you cannot attend and provide a brief explaination.')
    youtube_link = models.CharField('YouTube Link', max_length=60, help_text='Make sure the video is marked \'Unlisted\' and that all material is compiled into one video.', validators=[RegexValidator('youtube\.com/watch\?v=.+|youtu\.be/.+','Enter a valid YouTube link')])
    ranking = models.CharField('Ranking', max_length=15, choices=RANKING_CHOICES, default='Unassigned')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES,
                              default='Undetermined')
    confirmation = models.CharField(max_length=12, choices=CONFIRMATION_CHOICES,
                                    default='Unconfirmed')
    code = models.CharField(max_length=40, blank=True)
    submission_date_time = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        #change to 'include' style when first audition is over 
        exclude = ['status', 'ranking', 'confirmation', 'code']


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


