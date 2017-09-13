import re

from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

from AuditiON.models import Applicant, Instruments, Principal
from AuditiON.constants import get_brian_username
from django.http import HttpResponse, HttpResponseRedirect

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


def deny_brian(unicode_username):
    if (unicode_username == get_brian_username()):
        return True
    else:
        return False

def get_filtered_db_info(data):
    """ Filters info for db_info page display """
    query = Applicant.objects.all()
    if (data['instrument'] != 'Ignore'):
        instrument = Instruments.objects.get(name=data['instrument'])
        query = query.filter(instrument__exact=instrument)
    if (data['status'] != 'Ignore'):
        query = query.filter(status__exact=data['status'])
    if (data['confirmation'] != 'Ignore'):
        query = query.filter(confirmation__exact=data['confirmation'])
    if (data['availability'] != 'Ignore'):
        query = query.filter(availability__exact=data['availability'])

    query = query.order_by('last_name')

    return query

def get_instrument_list():
    x = []
    return x 
def hackget_instrument_list():
    """ Returns a list of tuples for choices in Applicant Instruments"""

    instrument_list = []
    instrument = Instruments.objects.all()
    for inst in instrument:
        instrument_tuple = (inst, inst)
        instrument_list.append(instrument_tuple)
    return instrument_list

def get_judge_ins_list(judge):
    x = []
    return x
def hackget_judge_ins_list(judge):
    """ Returns a list of tuples for choices in Applicant Instruments"""
    
    instrument_list = []
    instrument = judge.ins.all()
    for inst in instrument:
        instrument_tuple = (inst.name, inst.name)
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
    x = []
    return x
def hackget_applicant_list():
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



