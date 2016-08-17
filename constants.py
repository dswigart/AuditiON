
# Availability choices
AVAIL_ALL = 'All'
AVAIL_SOME = 'Some'

#Each of these has 'one-to-one' relationship with
#judges in User model.
FLUTE = 'Flute'
OBOE = 'Oboe'
ENGLISHHORN = 'EnglishHorn'
CLARINET = 'Clarinet'
BASSCLARINET = 'BassClarinet'
BASSOON = 'Bassoon'
FRENCHHORN = 'FrenchHorn'
TRUMPET = 'Trumpet'
TROMBONE = 'Trombone'
BASSTROMBONE = 'BassTrombone'
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