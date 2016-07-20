


# Availability choices
AVAIL_ALL = 'All'
AVAIL_SOME = 'Some'

# Constants for
FLUTE = 'fl'
OBOE = 'ob'
CLARINET = 'cl'
BASSOON = 'bn'
HORN = 'hn'
TRUMPET = 'tp'
TROMBONE = 'tb'
TUBA = 'tu'
TIMPANI = 'ti'
PERCUSSION = 'pn'
KEYBOARDS = 'kb'
HARP = 'hp'
VIOLIN = 'vi'
VIOLA = 'vo'
CELLO = 'ce'
BASS = 'ba'

#Each of these has 'one-to-one' relationship with
#judges in User model.
INSTRUMENT_LOOKUP = {
    'Flute':FLUTE,
    'Oboe':OBOE,
    'Clarinet':CLARINET,
    'Bassoon':BASSOON,
    'Horn':HORN,
    'Trumpet':TRUMPET,
    'Trombone':TROMBONE,
    'Tuba':TUBA,
    'Timpani':TIMPANI,
    'Percussion':PERCUSSION,
    'Keyboards':KEYBOARDS,
    'Harp':HARP,
    'Violin':VIOLIN,
    'Viola':VIOLA,
    'Cello':CELLO,
    'Bass':BASS
}


AVAILABILITY_LIST = (
    (AVAIL_ALL, 'All'),
    (AVAIL_SOME, 'Some'),
    )

#for use in forms
INSTRUMENT_LIST = (
    (FLUTE, 'Flute'),
    (OBOE, 'Oboe'),
    (CLARINET, 'Clarinet'),
    (BASSOON, 'Bassoon'),
    (HORN, 'Horn'),
    (TRUMPET, 'Trumpet'),
    (TROMBONE, 'Trombone'),
    (TUBA, 'Tuba'),
    (TIMPANI, 'Timpani'),
    (PERCUSSION, 'Percussion'),
    (KEYBOARDS, 'Keyboards'),
    (HARP, 'Harp'),
    (VIOLIN, 'Violin'),
    (VIOLA, 'Viola'),
    (CELLO, 'Cello'),
    (BASS, 'Bass'),
    )

LOCK = (
        ('Unlocked', 'Unlocked'),
        ('Locked', 'Locked'),
        )

PART_CHOICES = (
    ('Unassigned', 'Unassigned'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    )

STATUS_CHOICES = (
    ('Rejected', 'Rejected'),
    ('Accepted', 'Accepted'),
    ('Alternate', 'Alternate'),
    )

CONFIRMATION_CHOICES = (
    ('Unconfirmed', 'Unconfirmed'),
    ('Accept', 'Accept'),
    ('Reject', 'Reject'),
    )