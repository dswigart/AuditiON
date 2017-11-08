
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from AuditiON.models import StockEmailData

class EmailHelper:
    """ Helps with preparing collections of email objects """

    def _get_fields(self, email_title):
        ###handle possible errors (fix)
        fields = StockEmailData.objects.get(email_name=email_title)
        return fields


    def _process_confirmation_link(self, code):
        link = 'https://www.sarahviens.com/AuditiON/applicant_confirmation/'
        link += '?code=%s' % code
        return link


    def accepted_applicant_conf(self, applicant_queryset):
        fields = self._get_fields('accepted_confirmation')
        messages = []
        for obj in applicant_queryset:
            message = ''
            message += 'Dear %s,<br><br>' % obj.first_name
            message += '%s<br><br><br>' % fields.content_body
            message += self._process_confirmation_link(obj.code)
            message += '<br><br><br>We\'re very excited for this season!<br><br>Cheers!<br><br>Brian McWhorter, music director<br>Sarah Viens, trumpet/administration<br>www.orchestranext.com'
            email = EmailMessage(fields.subject_line, message, 'orchestranext@gmail.com',[obj.email_address])
            email.content_subtype = 'html'
            messages.append(email)
        return messages


    def rejected_applicant(self, applicant_queryset):
        fields = self._get_fields('test')
        messages = []
        for obj in applicant_queryset:
            message = ''
            message += '%s, \n\n' % obj.first_name
            message += '%s\n' % fields.content_body
            email = EmailMessage(fields.subject_line, message, 'dswigart@gmail.com',[obj.email_address])
            messages.append(email)
        return messages
