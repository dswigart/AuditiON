from django.test import TestCase

from AuditiON.models import AuditionControl, Applicant


# form data defaults are not included
VALID_APPLICANT = {'first_name':'Jim', 'last_name':'Brown', 'phone_number':'5621172675','email_address':'jimb@gsmail.com', 'street':'471 E. Devin', 'city':'Flint', 'zip_code':'44672', 'age':'20', 'school':'Lincoln High school', 'instrument':'fl', 'availability':'All', 'avail_explain':'no info givent', 'youtube_link':'www.youtube.com', }


# form data defaults are not included
INVALID_APPLICANT = {'first_name':'Jim', 'last_name':'Brown', 'phone_number':'5621172675','email_address':'jimmail.com', 'street':'471 E. Devin', 'city':'Flint', 'zip_code':'44672', 'age':'', 'school':'Lincoln High school', 'instrument':'fl', 'availability':'All', 'avail_explain':'no info givent', 'youtube_link':'www.youtube.com', }


class ApplicantFormUnlocked(TestCase):
    """ Tests that audition_form behaves correctly when unlocked """
    def setUp(self):
        controls = AuditionControl(reference_name='controls',
                                   applicant_form_lock='Unlocked',judge_submission_form_lock='Unlocked')
        controls.save()
    

    def test_index(self):
        response = self.client.get('/AuditiON/')
        self.assertEqual(response.status_code, 302)
        
        # 'assertRedirects' hack.
        self.assertEqual(response._headers['location'][1], 'audition_form')
    
    
    # normal access
    def test_audition_form_get(self):
        response = self.client.get('/AuditiON/audition_form')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/form.html')


    # form is not valid, loads page again with errors
    def test_audition_form_invalid_post(self):
        response = self.client.post('/AuditiON/audition_form')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/form.html')
        self.assertContains(response, 'errorlist')
    
    # form is valid, loads confirmation page
    def test_audition_form_valid_post(self):
     
        response = self.client.post('/AuditiON/audition_form', VALID_APPLICANT)
        self.assertNotContains(response, 'errorlist')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/form_confirmation.html')
        
        # test for all form data
        for x in VALID_APPLICANT:
            self.assertContains(response, x)


    def tearDown(self):
        AuditionControl.objects.all().delete()
        Applicant.objects.all().delete()

class ApplicantFormLocked(TestCase):
    """ Tests that audition_form behaves correctly when locked """
    def setUp(self):
        controls = AuditionControl(reference_name='controls',
                    applicant_form_lock='Locked',judge_submission_form_lock='Unlocked')
        controls.save()
    
    
    def test_index(self):
        response = self.client.get('/AuditiON/')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 200)
        
        # 'assertRedirects' hack.
        self.assertEqual(response._headers['location'][1], 'audition_form')
    
    
    def test_audition_form_get(self):
        response = self.client.get('/AuditiON/audition_form')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response._headers['location'][1], 'audition_closed')
        
        
    def test_audition_form_post(self):
        response = self.client.post('/AuditiON/audition_form')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response._headers['location'][1], 'audition_closed')
        
    
    def test_audition_closed(self):
        response = self.client.get('/AuditiON/audition_closed')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/audition_closed.html')


    def tearDown(self):
        AuditionControl.objects.all().delete()


class AuditionFormConfirmationUnlocked(TestCase):
    """ Tests if audition_confirmation behaves correctly when unlocked """
    def setUp(self):
        controls = AuditionControl(reference_name='controls',
                                   applicant_form_lock='Unlocked',judge_submission_form_lock='Unlocked')
        controls.save()
    
    
    # get should redirect
    def test_audition_confirmation_get(self):
        response = self.client.get('/AuditiON/audition_form_confirmation')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response._headers['location'][1], 'access_denied')
    
    
    # no form data
    def test_audition_confirmation_post(self):
        response = self.client.post('/AuditiON/audition_form_confirmation')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/form.html')
    
    
    def test_invalid_form(self):
        response = self.client.post('/AuditiON/audition_form_confirmation', INVALID_APPLICANT)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/form.html')
        self.assertContains(response, 'errorlist')
    
    def test_valid_form(self):
        response = self.client.post('/AuditiON/audition_form_confirmation', VALID_APPLICANT)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'AuditiON/form_success.html')
        self.assertEqual(response._headers['location'][1], 'form_success')
        
        # check that data was saved
        x = Applicant.objects.get(email_address=VALID_APPLICANT['email_address'])
        self.assertEqual(VALID_APPLICANT['phone_number'], x.phone_number)
    
    
    def tearDown(self):
        AuditionControl.objects.all().delete()
        Applicant.objects.all().delete()


class AuditionFormConfirmationLocked(TestCase):
    """ Tests if audition_confirmation behaves correctly when locked """
    def setUp(self):
        controls = AuditionControl(reference_name='controls',
                                   applicant_form_lock='Locked',judge_submission_form_lock='Unlocked')
        controls.save()


    def test_audition_form_confirmation_get(self):
        response = self.client.get('/AuditiON/audition_form_confirmation')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response._headers['location'][1], 'audition_closed')
    
    
    def test_audition_form_confirmation_post(self):
        response = self.client.post('/AuditiON/audition_form_confirmation')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response._headers['location'][1], 'audition_closed')


    # already tested 'audition_closed' above


    def tearDown(self):
        AuditionControl.objects.all().delete()
        Applicant.objects.all().delete()


class JudgeSubmissionFormLocked(TestCase):
    def setUp(self):
        controls = AuditionControl(reference_name='controls',
                    applicant_form_lock='Locked', judge_submission_form_lock='Locked')
        controls.save()


    def test_judge_submission_form(self):
        response = self.client.get('/AuditiON/applicant_selection')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], 'access_denied')

    def tearDown(self):
        AuditionControl.objects.all().delete()






























