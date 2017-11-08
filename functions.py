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


# Can't be moved into models.py?
def get_judge_list():
    judge_list = []
    judges = User.objects.all()
    for judge in judges:
        judge_tuple = (judge, judge)
        judge_list.append(judge_tuple)
    return judge_list
