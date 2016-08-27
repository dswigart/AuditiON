from django.test import TestCase
from django.contrib.auth.models import User
from django.forms import modelformset_factory

from AuditiON.models import AuditionControl, Applicant, ApplicantForm


# form data defaults are not included
VALID_APPLICANT = {'first_name':'Jim', 'last_name':'Brown', 'phone_number':'5621172675','email_address':'jimb@gsmail.com', 'zip_code':'44672', 'age':'20', 'school':'Lincoln High school', 'instrument':'Flute', 'availability':'All', 'avail_explain':'no info given', 'youtube_link':'67e4v5TY', }


# form data defaults are not included
VALID_APPLICANT_FLUTE = {'first_name':'Diva', 'last_name':'Girarda', 'phone_number':'5621172675', 'email_address':'jimb@gsmail.com', 'zip_code':'44672', 'age':'20', 'school':'Lincoln High school', 'instrument':'Flute', 'availability':'All', 'avail_explain':'no info given', 'youtube_link':'hf5GY76U8', }


# form data defaults are not included
VALID_APPLICANT_TWO = {'first_name':'Steve', 'last_name':'Diant', 'phone_number':'5621172675','email_address':'st@gsmail.com', 'zip_code':'44672', 'age':'20', 'school':'Lincoln High school', 'instrument':'Trumpet', 'availability':'All', 'avail_explain':'no info given', 'youtube_link':'jf5G62S4n', }


# form data defaults are not included
INVALID_APPLICANT = {'first_name':'Jim', 'last_name':'Brown', 'phone_number':'5621172675','email_address':'jimmail.com', 'zip_code':'44672', 'age':'', 'school':'Lincoln High school', 'instrument':'fl', 'availability':'All', 'avail_explain':'no info given', 'youtube_link':'www.youtube.com', }


class ApplicantFormMissingControls(TestCase):
    """ Tests redirect if controls are missing """
    def test_index(self):
        response = self.client.get('/AuditiON/audition_form')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/AuditiON/database_problem')


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
        self.assertEqual(response._headers['location'][1], '/AuditiON/audition_form')
    
    
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
        self.assertEqual(response._headers['location'][1], '/AuditiON/audition_form')
    
    
    def test_audition_form_get(self):
        response = self.client.get('/AuditiON/audition_form')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response._headers['location'][1], '/AuditiON/audition_closed')
        
        
    def test_audition_form_post(self):
        response = self.client.post('/AuditiON/audition_form')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response._headers['location'][1], '/AuditiON/audition_closed')
        
    
    def test_audition_closed(self):
        response = self.client.get('/AuditiON/audition_closed')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/audition_closed.html')


    def tearDown(self):
        AuditionControl.objects.all().delete()


class AuditionConfirmationMissingControls(TestCase):
    """ Tests redirect if controls are missing """
    def test_index(self):
        response = self.client.get('/AuditiON/audition_form_confirmation')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/AuditiON/database_problem')


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
        self.assertEqual(response._headers['location'][1], '/AuditiON/access_denied')
    
    
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
        self.assertEqual(response._headers['location'][1], '/AuditiON/form_success')
        
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
        self.assertEqual(response._headers['location'][1], '/AuditiON/audition_closed')
    
    
    def test_audition_form_confirmation_post(self):
        response = self.client.post('/AuditiON/audition_form_confirmation')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response._headers['location'][1], '/AuditiON/audition_closed')


    # already tested 'audition_closed' above


    def tearDown(self):
        AuditionControl.objects.all().delete()
        Applicant.objects.all().delete()


class JudgeLogin(TestCase):
    """ Tests correct redirect on various use cases """
    def setUp(self):
        current_user = User.objects.create_user('Flute','dswigart@gmail.com','12345')
    
    
    # Reload page with error message
    def test_user_not_in_database(self):
        response = self.client.post('/AuditiON/judge_login', {'username':'NotInDB', 'password':'blaaa'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/judge_login.html')
        self.assertContains(response, 'Your username and password didn\'t match')
        with self.assertRaises(KeyError):
            response._headers['location']


    # Reload page with error message
    def test_user_bad_password(self):
        response = self.client.post('/AuditiON/judge_login', {'username':'Flute', 'password':'blaaa'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/judge_login.html')
        self.assertContains(response, 'Your username and password didn\'t match')
        with self.assertRaises(KeyError):
            response._headers['location']


    # Reload page with error message
    def test_bad_user_good_password(self):
        response = self.client.post('/AuditiON/judge_login', {'username':'NotInDB', 'password':'12345'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/judge_login.html')
        self.assertContains(response, 'Your username and password didn\'t match')
        with self.assertRaises(KeyError):
            response._headers['location']
    

    # Redirect upon successful login
    def test_successful_login(self):
        response = self.client.post('/AuditiON/judge_login', {'username':'Flute', 'password':'12345'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/AuditiON/applicant_list')


    # Load login page
    def test_get(self):
        response = self.client.get('/AuditiON/judge_login')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/judge_login.html')
    
    
    def tearDown(self):
        User.objects.all().delete()
                                    

class JudgeLogout(TestCase):
    """ Test logout use cases """
    def setUp(self):
        current_user = User.objects.create_user('Flute','dswigart@gmail.com','12345')
    
    # Redirect back to login page
    def test_user_logout(self):
        # Verify login
        self.assertTrue(self.client.login(username='Flute', password='12345'))
        self.assertNotEqual(self.client.session.items(), [])
        
        # Verify redirect
        response = self.client.get('/AuditiON/judge_logout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/AuditiON/judge_login')
        
        # Verify logout
        self.assertEqual(self.client.session.items(), [])

    # Redirect back to login page
    def test_user_already_logged_out(self):
        response = self.client.get('/AuditiON/judge_logout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/AuditiON/judge_login')
        
        # Verify logout
        self.assertEqual(self.client.session.items(), [])


    def tearDown(self):
        User.objects.all().delete()


class ApplicantList(TestCase):
    def setUp(self):
        current_user = User.objects.create_user('Flute','dswigart@gmail.com','12345')
        applicant = ApplicantForm(VALID_APPLICANT)
        applicant.save()
        applicant = ApplicantForm(VALID_APPLICANT_TWO)
        applicant.save()


    # Redirect to access_denied
    def test_user_not_logged_in(self):
        response = self.client.get('/AuditiON/applicant_list')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/AuditiON/access_denied')


    def test_user_logged_in(self):
        # Verify login
        self.assertTrue(self.client.login(username='Flute', password='12345'))
        self.assertNotEqual(self.client.session.items(), [])
        
        response = self.client.get('/AuditiON/applicant_list')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/applicant_list.html')


    # test_user_not_in_database is unnecessary, end-user can't get this
    # far if not in database


    def test_applicant_loading(self):
        # Verify login
        self.assertTrue(self.client.login(username='Flute', password='12345'))
        self.assertNotEqual(self.client.session.items(), [])
        
        # Applicant objects returned should correspond to username
        response = self.client.get('/AuditiON/applicant_list')
        app_list = response.context['applicant_list']
        user = response.context['user']
        for x in app_list:
            self.assertEqual(user.get_username(), x.instrument)

        # Verify that non-matching applicants exist
        all_applicants = Applicant.objects.all()
        self.assertNotEqual(len(app_list), len(all_applicants))


    def tearDown(self):
        Applicant.objects.all().delete()
        User.objects.all().delete()


class ApplicantSelectionMissingControls(TestCase):
    """ Tests redirect if controls are missing """
    def test_index(self):
        response = self.client.get('/AuditiON/applicant_selection')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/AuditiON/database_problem')


class ApplicantSelectionFormLocked(TestCase):
    """ Tests applicant_selection when locked """
    def setUp(self):
        controls = AuditionControl(reference_name='controls',
                    applicant_form_lock='Locked', judge_submission_form_lock='Locked')
        controls.save()


    def test_judge_submission_form(self):
        response = self.client.get('/AuditiON/applicant_selection')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/AuditiON/access_denied')


    def tearDown(self):
        AuditionControl.objects.all().delete()


class ApplicantSelectionUnlockedGet(TestCase):
    """ Tests 'normal' use cases """
    def setUp(self):
        controls = AuditionControl(reference_name='controls',
                                   applicant_form_lock='Locked', judge_submission_form_lock='Unlocked')
        controls.save()
        current_user = User.objects.create_user('Flute','dswigart@gmail.com','12345')
        applicant = ApplicantForm(VALID_APPLICANT)
        applicant.save()
        applicant = ApplicantForm(VALID_APPLICANT_TWO)
        applicant.save()
        applicant = ApplicantForm(VALID_APPLICANT_FLUTE)
        applicant.save()
    
    # Redirect to access_denied
    def test_user_not_logged_in(self):
        response = self.client.get('/AuditiON/applicant_selection')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/AuditiON/access_denied')


    def test_applicant_get(self):
        # Verify login
        self.assertTrue(self.client.login(username='Flute', password='12345'))
        self.assertNotEqual(self.client.session.items(), [])
        
        # Applicant objects returned should correspond to username
        response = self.client.get('/AuditiON/applicant_selection')
        formset = response.context['set']
        app_queryset = formset.get_queryset()
        user = response.context['user']
        for x in app_queryset:
            self.assertEqual(user.get_username(), x.instrument)

        # Verify that non-matching applicants exist
        all_applicants = Applicant.objects.all()
        self.assertNotEqual(len(app_queryset), len(all_applicants))
        
        # load appropriate template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/applicant_selection.html')


    def test_applicant_post(self):
        # Verify login
        self.assertTrue(self.client.login(username='Flute', password='12345'))
        self.assertNotEqual(self.client.session.items(), [])
        
        # shortcut to verifying applicant's status
        response = self.client.get('/AuditiON/applicant_selection')
        formset = response.context['set']
        app_queryset = formset.get_queryset()
        for x in app_queryset:
            self.assertEqual(x.status, 'Rejected')
        
        # altering status on one applicant (there are two in the set)
        

        # confirming status change
        applicant = Applicant.objects.filter(instrument__exact='Flute')
        self.assertNotEqual(applicant[0].status, applicant[1].status)
    


    def tearDown(self):
        Applicant.objects.all().delete()
        User.objects.all().delete()
        AuditionControl.objects.all().delete()



class ApplicantConfirmationGet(TestCase):
    """ Test all GET use cases for applicant_confirmation """
    def setUp(self):
        applicant = ApplicantForm(VALID_APPLICANT)
        applicant.save()


    # page not should be accessed without code
    def test_no_code(self):
        response = self.client.get('/AuditiON/applicant_confirmation')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/AuditiON/access_denied')
    

    # redirect to database_problem
    def test_bad_code(self):
        response = self.client.get('/AuditiON/applicant_confirmation/?code=1234567')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/AuditiON/database_problem')


    # redirect to limit each 'user' to one submit
    def test_already_confirmed(self):
        applicant = Applicant.objects.get(instrument='Flute')
        applicant.confirmation='Accept'
        applicant.save()
        
        url = '/AuditiON/applicant_confirmation/?code=%s' % applicant.code
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/AuditiON/already_confirmed')


    # ideal use case
    def test_not_confirmed(self):
        applicant = Applicant.objects.get(instrument='Flute')
        applicant.confirmation='Unconfirmed'
        applicant.save()

        url = '/AuditiON/applicant_confirmation/?code=%s' % applicant.code
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AuditiON/applicant_confirmation.html')


    def tearDown(self):
        Applicant.objects.all().delete()


class ApplicantConfirmationPost(TestCase):
    """ Test POST use cases for applicant_confirmation """
    def setUp(self):



