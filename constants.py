

# Availability choices
AVAIL_ALL = 'All'
AVAIL_SOME = 'Some'

AVAILABILITY_LIST = (
    (AVAIL_ALL, 'All'),
    (AVAIL_SOME, 'Some'),
    )

YES_NO = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    )

def ADD_IGNORE(tuple):
    list = []
    list.append(('Ignore', '---'))
    for x in tuple:
        list.append(x)
    return list


def get_brian_username():
    name = 'boiledjar'
    return unicode(name)


LOCK = (
        ('Unlocked', 'Unlocked'),
        ('Locked', 'Locked'),
        )

RANKING_CHOICES = (
    ('Unassigned', 'Unassigned'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
    )

STATUS_CHOICES = (
    ('Undetermined', 'Undetermined'),
    ('Declined', 'Declined'),
    ('Accepted', 'Accepted'),
    ('Alternate', 'Alternate'),
    )

CONFIRMATION_CHOICES = (
    ('Unconfirmed', 'Unconfirmed'),
    ('Accept', 'Accept'),
    ('Decline', 'Decline'),
    )
