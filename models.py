
from django.db import models

from django.forms import ModelForm
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from AuditiON.constants import AVAILABILITY_LIST, CONFIRMATION_CHOICES, STATUS_CHOICES, RANKING_CHOICES, LOCK, YES_NO

# hack 'UniqueUsername': neccesary in order to keep superusers and users from having the same name.
# fixes: the system may load one when the other was intended--now it cannot.
User._meta.get_field('username')._unique = True


class Legacy(models.Model):
    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    phone_number = models.CharField('Phone Number', max_length=17)
    email_address = models.EmailField('Email Address')
    zip_code = models.CharField('Zip Code', max_length=5)


class InstrumentManager(models.Manager):
    """ Custom Manager methods for instrument collections in forms"""
    def get_queryset(self):
        return super(InstrumentManager, self).get_queryset().order_by('score_order')

    def get_instrument_list(self):
        """ Returns a list of tuples for choices"""
        instrument = self.model.objects.all().values_list('name', 'name')
        return instrument

    def get_judge_ins_list(self, judge):
        """ Returns a list of tuples for choices"""
        instrument = judge.ins.all().values_list('name', 'name')
        return instrument


class Instruments(models.Model):
    """ Instruments """
    name = models.CharField('Instrument Name', max_length=30, primary_key=True)
    judge = models.ForeignKey(User, related_name='ins', on_delete=models.SET_NULL, null=True, blank=True)
    score_order = models.IntegerField('Score Ordering')

    objects = InstrumentManager()
    custom = InstrumentManager()

    def __str__(self):
        return self.name


class CreateInstrument(ModelForm):
    class Meta:
        model = Instruments
        fields = ['name', 'score_order']


class PrincipalManager(models.Manager):

    def get_principal_list(self):
        """ Returns a list of tuples for choices """
        principal_list = []
        return principal_list
        '''principals = self.model.objects.all()
        for principal in principals:
            display = '%s %s, %s' % (principal.first_name, principal.last_name, principal.instrument)
            principal_tuple = (principal.code, display)
            principal_list.append(principal_tuple)
        return principal_list'''


class Principal(models.Model):

    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    email_address = models.EmailField('Email Address')
    instrument = models.ForeignKey(Instruments, related_name='prin', on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=40, blank=True)

    objects = models.Manager()
    custom = PrincipalManager()

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class PrincipalEditForm(ModelForm):
    class Meta:
        model = Principal
        fields = '__all__'


class CreatePrincipal(ModelForm):
    class Meta:
        model = Principal
        fields = '__all__'


class ApplicantManager(models.Manager):

    def get_applicant_list(self):
        """ Returns a list of tuples for choices """
        applicant_list = []
        return applicant_list

        '''applicants = self.model.objects.all().order_by('last_name')
        for applicant in applicants:
            display = '%s %s, %s' % (applicant.first_name, applicant.last_name, applicant.instrument)
            applicant_tuple = (applicant.code, display)
            applicant_list.append(applicant_tuple)
        return applicant_list'''


class Applicant(models.Model):
    """ Main data for Orchestra applicants """

    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    phone_number = models.CharField('Phone Number', max_length=17)
    email_address = models.EmailField('Email Address')
    zip_code = models.CharField('Zip Code', max_length=5)
    age = models.CharField('Age', max_length=3)
    instrument = models.ForeignKey(Instruments, on_delete=models.SET_NULL, null=True, blank=True)
    school = models.CharField('School', max_length=40)
    youtube_link = models.CharField('YouTube Link', max_length=60, help_text='(one video, all excerpts compiled)', validators=[RegexValidator('youtube\.com/watch\?v=.+|youtu\.be/.+','Enter a valid YouTube link')])
    availability = models.CharField('Availability', max_length=6,
                                    choices=AVAILABILITY_LIST)
    avail_explain = models.TextField('Availability Explaination', default='All', help_text='If \'some\' was marked above, please note rehearsals or shows you cannot attend and provide a brief explaination.')
    work_eligibility = models.CharField('Are you eligible to work in the USA?', max_length=6, choices=YES_NO)
    ranking = models.CharField('Ranking', max_length=15, choices=RANKING_CHOICES, default='Unassigned')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Undetermined')
    confirmation = models.CharField(max_length=12, choices=CONFIRMATION_CHOICES, default='Unconfirmed')
    code = models.CharField(max_length=40, blank=True)
    submission_date_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    custom = ApplicantManager()

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        #change to 'include' style when first audition is over
        exclude = ['status', 'ranking', 'confirmation', 'code']


class ApplicantEditForm(ModelForm):
    class Meta:
        model = Applicant
        #change to 'include' style when first audition is over
        fields = '__all__'


class ProductionData(models.Model):
    # note: name should be set to 'production_data'
    name = models.CharField(max_length=18, primary_key=True)
    data = models.TextField('Production Data')

class ProductionDataForm(ModelForm):
    class Meta:
        model = ProductionData
        fields = '__all__'


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

class StockEmailDataForm(ModelForm):
    class Meta:
        model = StockEmailData
        fields = '__all__'
