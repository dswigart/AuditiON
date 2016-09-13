import re

from AuditiON.models import Applicant


def youtube_split(link):
    """ Formats youtube string to embed in site """
    # Determine if 'youtube.com/watch?=xxxxxxxx' format and process
    match = re.search(r"youtube.com", link)
    if (match):
        x = re.search("\=\w+", link)
        x = x.group(0)
        slice = x[1:]
        return slice
    
    # Determine if 'youtu.be/xxxxxxx' format and process
    match = re.search(r"youtu.be", link)
    if (match):
        x = re.search("be/\w+", link)
        x = x.group(0)
        slice = x[3:]
        return slice


def get_filtered_db_info(data):
    query = Applicant.objects.all()
    if (data['instrument'] != 'Ignore'):
        query = query.filter(instrument__exact=data['instrument'])
    if (data['status'] != 'Ignore'):
        query = query.filter(status__exact=data['status'])
    if (data['confirmation'] != 'Ignore'):
        query = query.filter(confirmation__exact=data['confirmation'])
    if (data['availability'] != 'Ignore'):
        query = query.filter(availability__exact=data['availability'])
    return query