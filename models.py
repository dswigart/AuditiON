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
    street = models.CharField('Street Address', max_length=40)
    city = models.CharField('City', max_length=40)
    zip_code = models.PositiveSmallIntegerField('Zip Code')
    age = models.IntegerField('Age')
    school = models.CharField('School', max_length=40)
    instrument = models.CharField('Instrument', max_length=2,
                                    choices=INSTRUMENT_LIST)
    availability = models.CharField('Availability', max_length=6,
                                    choices=AVAILABILITY_LIST)
    avail_explain = models.TextField('Availability Explaination',
                                     default='no info given')
    youtube_link = models.TextField('YouTube Link', default='no info given',
                            validators=[RegexValidator('(www.)?youtu(be.com|.be)',
                                                       'Enter a valid YouTube link')])
    part = models.CharField(max_length=1, choices=PART_CHOICES, default='Unassigned')
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








class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    def __str__(self):
        return self.headline
