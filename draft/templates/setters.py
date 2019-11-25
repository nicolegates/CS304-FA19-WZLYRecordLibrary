import dbi
from add import *

def getConn(db):
    '''Returns a database connection for that db'''
    dsn = dbi.read_cnf()
    conn = dbi.connect(dsn)
    conn.select_db(db)
    return conn

def insertAlbum(name, artist, conn):
    '''takes a user-inputted album and
    adds it to the album table'''
    
    try:
        name = fixThes(name, ', the')
        name = fixThes(name, ',the')
        artist = fixThes(artist, ',the')
        artist = fixThes(artist, ', the')

        curs = dbi.dictCursor(conn)
        curs.execute('insert into album (name, artist, fmt) ' +\
                     'values (%s, %s, %s)', [name, artist, 'cd'])
    except:
        return False

# def insertTracks(track, num, conn):
#     '''takes a list of tracks and updates
#     the track table'''

# def insertGenre(genre, aid, conn):
#     '''inserts a genre/album pair into
#     the genre table'''
