alliance_clubs = ['28GLU0CU9', '22LJV2GUQ']


def emoji(desc):
    D = {
        'hash': '#️⃣',
        'person': chr(128100),
        'trophy': chr(127942),
        'error': chr(10060),
        'ok': chr(9989),
        'kaif': chr(129305),
        'blue': chr(128309)
    }
    return D.get(desc, D['error'])

playerUpdateDelay = 20
clubUpdateDelay = 200