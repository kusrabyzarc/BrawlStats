alliance_clubs = ['28GLU0CU9', '22LJV2GUQ']


def emoji(desc):
    D = {
        'hash': '#️⃣',
        'person': chr(128100),
        'trophy': chr(127942),
        'error': chr(128683)
    }
    return D.get(desc, D['error'])