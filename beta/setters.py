import dbi
from add import *
from datetime import date
from datetime import timedelta

def insertAlbum(name, artist, conn):
    '''takes a user-inputted album and
    adds it to the album table. If the insert
    fails, returns None.'''
    
    try:
        name = fixThes(name, ', the')
        name = fixThes(name, ',the')
        artist = fixThes(artist, ',the')
        artist = fixThes(artist, ', the')

        curs = dbi.dictCursor(conn)
        curs.execute('''insert into album (name, artist, fmt)
                        values (%s, %s, %s)''',
                        [name, artist, 'cd'])
        curs.execute('select LAST_INSERT_ID()')
        aid = curs.fetchone()
        return aid
    except:
        return None

def updateAlbum(aid, name, artist, year,
                fmt, location, art, embed,
                spotify_album_id, conn):
    '''Updates an album. Returns True if
    successful, False if not.'''
    curs = dbi.dictCursor(conn)
    
    try:
        curs.execute('''update album
                        set name = %s, artist = %s, year = %s,
                        fmt = %s, location = %s, art = %s, embed = %s,
                        spotify_album_id = %s
                        where aid = %s;''',
                        [name, artist, year, fmt, location,
                        art, embed, spotify_album_id, aid])
        return True
    except:
        return False
    
def deleteAlbum(aid, conn):
    '''deletes an album from the album table'''
    curs = dbi.dictCursor(conn)
    curs.execute('delete from album where aid = %s', [aid])

def checkout(aid, bid, conn):
    '''given an album ID and a banner ID, adds a reservation
    to the reservation table and returns the due date'''
    today = date.today()
    due = today + timedelta(30)

    curs = dbi.dictCursor(conn)
    curs.execute('''insert into reservation
                        (checkout, due, returned, aid, bid)
                    values (%s, %s, %s, %s, %s);''',
                    [today, due, 0, aid, bid])
    return due

def checkin(rid, conn):
    '''given a reservation ID, updates
    a reservation as having been returned. Returns
    the name of the album returned.'''

    curs = dbi.dictCursor(conn)
    
    try:
        curs.execute('''update reservation
                        set returned = 1 where rid = %s;''',
                        [rid])
        curs.execute('''
                    select album.name
                        from reservation
                    inner join album
                        on reservation.aid = album.aid
                    where reservation.rid = %s;
                    ''', [rid])
        album = curs.fetchone()
        return album['name']
    except:
        return None

def checkUser(bid, name, username, conn):
    '''Checks whether a person is already in the
    person table. If they are, returns False, 
    if they are not, inserts them and returns True.'''
    
    curs = dbi.dictCursor(conn)

    curs.execute('select * from person where bid = %s', [bid])
    res = curs.fetchone()
    if res is not None:
        return False
    else:
        curs.execute('insert into person (bid, name, username, is_admin)' +\
                     'values (%s, %s, %s, 0)', [bid, name, username])
        return True
    

def insertTracks(aid, tracks, conn):
    '''takes a user-inputted list of tracks
    and updates the track table'''
    tracklist = tracks.splitlines()
    curs = dbi.dictCursor(conn)

    num = 1
    for t in tracklist:
        curs.execute('insert into track (name, num, aid)' +\
                     'values (%s, %s, %s)', [t, num, aid])
        num += 1

def insertGenres(aid, genres, conn):
    '''inserts genre/album pairs into
    the genre table'''
    genrelist = genres.splitlines()
    curs = dbi.dictCursor(conn)

    for g in genrelist:
        curs.execute('insert into genre (name, aid)' +\
                     'values (%s, %s)', [g, aid])
