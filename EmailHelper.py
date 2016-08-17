from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from AuditiON.models import StockEmailData


class EmailHelper:
    """ Helps with preparing collections of email objects """

    def _get_fields(self, email_title):
        try:
            fields = StockEmailData.objects.get(email_name=email_title)
        except ObjectDoesNotExist:
            print('ObjectDoesNotExist: StockEmail missing')
        except MultipleObjectsReturned:
            print('MultipleObjectsReturned:  email_name should not be duplicated')
        return fields


    def _process_confirmation_link(self, code):
        link = 'http://localhost:8000/AuditiON/applicant_confirmation/'
        link += '?code=%s' % code
        return link
    
    
    def create_accepted_applicant_confirmation_request(self, applicant_queryset):
        fields = self._get_fields('test')
        messages = []
        for obj in applicant_queryset:
            message = ''
            message += '%s,\n\n' % obj.first_name
            message += '%s\n' % fields.content_body
            message += self._process_confirmation_link(fields.code)
            email = EmailMessage(fields.subject_line, message, 'orchestranext@gmail.com',[obj.email_address])
            messages.append(email)
        return messages


    def create_rejected_applicant_notification(self, applicant_queryset):
        fields = self._get_fields('test')
        messages = []
        for obj in applicant_queryset:
            message = ''
            message += '%s, \n\n' % obj.first_name
            message += '%s\n' % fields.content_body
            email = EmailMessage(fields.subject_line, message, 'dswigart@gmail.com',[obj.email_address])
            messages.append(email)
        return messages







