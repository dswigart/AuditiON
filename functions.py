import re


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