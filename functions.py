import re

from django.contrib.auth.models import User

from AuditiON.models import Applicant, Instruments, Principal


def youtube_split(link):
    """ Formats youtube string to embed in site """
    # Determine if 'youtube.com/watch?=xxxxxxxx' format and process
    match = re.search(r"youtube.com", link)
    if (match):
        x = re.search("\=.+", link)
        x = x.group(0)
        slice = x[1:]
        return slice
    
    # Determine if 'youtu.be/xxxxxxx' format and process
    match = re.search(r"youtu.be", link)
    if (match):
        x = re.search("be/.+", link)
        x = x.group(0)
        slice = x[3:]
        return slice


def get_filtered_db_info(data):
    """ Filters info for db_info page display """
    query = Applicant.objects.all()
    if (data['instrument'] != 'Ignore'):
        query = query.filter(instrument__exact=data['instrument'])
    if (data['status'] != 'Ignore'):
        query = query.filter(status__exact=data['status'])
    if (data['confirmation'] != 'Ignore'):
        query = query.filter(confirmation__exact=data['confirmation'])
    if (data['availability'] != 'Ignore'):
        query = query.filter(availability__exact=data['availability'])

    query = query.order_by('last_name')

    return query

def get_instrument_list():
    """ Returns a list of tuples for choices in Applicant Instruments"""

    instrument_list = []
    instruments = Instruments.objects.all()
    for ins in instruments:
        instrument_tuple = (ins, ins)
        instrument_list.append(instrument_tuple)

    return instrument_list


def get_judge_list():
    judge_list = []
    judges = User.objects.all()
    for judge in judges:
        judge_tuple = (judge, judge)
        judge_list.append(judge_tuple)

    return judge_list


def get_applicant_list():
    """ Returns a list of tuples for choices in Delete Applicant FIX THIS"""
    applicant_list = []
    applicants = Applicant.objects.all()
    for applicant in applicants:
        display = '%s %s, %s' % (applicant.first_name, applicant.last_name, applicant.instrument)
        applicant_tuple = (applicant.code, display)
        applicant_list.append(applicant_tuple)

    return applicant_list


def get_principal_list():
    """ Returns a list of tuples for choices in Delete Principal FIX THIS"""
    principal_list = []
    principals = Principal.objects.all()
    for principal in principals:
        display = '%s %s, %s' % (principal.first_name, principal.last_name, principal.instrument)
        principal_tuple = (principal.code, display)
        principal_list.append(principal_tuple)

    return principal_list



