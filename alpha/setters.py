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
        curs.execute('select aid from album where ' +\
                     'name = %s and artist = %s;', [name, artist])
        aid = curs.fetchone()
        return aid
    except:
        return None

def updateAlbum(aid, name, artist, year, fmt, location, art, embed, conn):
    '''Updates an album. Returns True if successful, False if not.'''
    curs = dbi.dictCursor(conn)
    
    try:
        curs.execute('update album ' +\
                    'set name = %s, artist = %s, year = %s, ' +\
                    'fmt = %s, location = %s, art = %s, embed = %s ' +\
                    'where aid = %s;',
                    [name, artist, year, fmt, location, art, embed, aid])
        return True
    except:
        return False
    
def deleteAlbum(aid, conn):
    '''deletes an album from the album table'''
    curs = dbi.dictCursor(conn)
    curs.execute('delete from album where aid = %s', [aid])


# def insertTracks(track, num, conn):
#     '''takes a list of tracks and updates
#     the track table'''

# def insertGenre(genre, aid, conn):
#     '''inserts a genre/album pair into
#     the genre table'''

# conn = getConn('cs304reclib_db')
# res = updateAlbum(18423, 'dumb album 1', 'dumb artist 1', 1997, 'cd', 'dumbloc', 'dumbart', 'embed', conn)
# print(res)