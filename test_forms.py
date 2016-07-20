from django.test import TestCase

from AuditiON.models import ApplicantForm, Applicant, AuditionControl


class ApplicantFormValidation(TestCase):
    def setUp(self):
        controls = AuditionControl(reference_name='controls',
                applicant_form_lock='Unlocked',judge_submission_form_lock='Unlocked')
        controls.save()
    
    
    def test_applicant_form_errors(self):
        response = self.client.post('/AuditiON/audition_form', {'first_name':''})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/form.html')
        self.assertContains(response, 'This field is required.')
