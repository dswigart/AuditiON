
# Availability choices
AVAIL_ALL = 'All'
AVAIL_SOME = 'Some'

#Each of these has 'one-to-one' relationship with
#judges in User model.
FLUTE = 'Flute'
OBOE = 'Oboe'
ENGLISHHORN = 'English Horn'
CLARINET = 'Clarinet'
BASSCLARINET = 'Bass Clarinet'
BASSOON = 'Bassoon'
FRENCHHORN = 'French Horn'
TRUMPET = 'Trumpet'
TROMBONE = 'Trombone'
BASSTROMBONE = 'Bass Trombone'
TUBA = 'Tuba'
TIMPANI = 'Timpani'
PERCUSSION = 'Percussion'
KEYBOARDS = 'Keyboards'
HARP = 'Harp'
VIOLIN = 'Violin'
VIOLA = 'Viola'
CELLO = 'Cello'
BASS = 'Bass'

AVAILABILITY_LIST = (
    (AVAIL_ALL, 'All'),
    (AVAIL_SOME, 'Some'),
    )

#for use in forms
INSTRUMENT_LIST = (
    (FLUTE, FLUTE),
    (OBOE, OBOE),
    (ENGLISHHORN, ENGLISHHORN),
    (CLARINET, CLARINET),
    (BASSCLARINET, BASSCLARINET),
    (BASSOON, BASSOON),
    (FRENCHHORN, FRENCHHORN),
    (TRUMPET, TRUMPET),
    (TROMBONE, TROMBONE),
    (BASSTROMBONE, BASSTROMBONE),
    (TUBA, TUBA),
    (TIMPANI, TIMPANI),
    (PERCUSSION, PERCUSSION),
    (KEYBOARDS, KEYBOARDS),
    (HARP, HARP),
    (VIOLIN, VIOLIN),
    (VIOLA, VIOLA),
    (CELLO, CELLO),
    (BASS, BASS),
    )


def ADD_IGNORE(tuple):
    list = []
    list.append(('Ignore', '---'))
    for x in tuple:
        list.append(x)
    return list


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