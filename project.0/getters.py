import dbi

def getConn(db):
    '''Returns a database connection for that db'''
    dsn = dbi.read_cnf()
    conn = dbi.connect(dsn)
    conn.select_db(db)
    return conn

def searchAlbums(query, conn):
    '''adds tracks and their order
    to track table'''

    curs = dbi.dictCursor(conn)
    curs.execute('select * from album where name like %s',
                ['%' + query + '%'])

    return curs.fetchall()

def searchArtists(query, conn):
    '''returns all artists matching a query'''

    curs = dbi.dictCursor(conn)
    curs.execute('select * from album ' +\
                 'where artist like %s',
                  ['%' + query + '%'])
    return curs.fetchall()

def searchYear(query, conn):
    '''returns all albums from given year'''

    curs = dbi.dictCursor(conn)
    curs.execute('select * from album ' +\
                 'where year = %s',
                  [query])
    return curs.fetchall()

def searchGenre(query, conn):
    '''returns all albums of a specific genre'''

    curs = dbi.dictCursor(conn)
    curs.execute('select * from album a ' +\
                 'inner join genre g ' +\
                    'on a.aid = g.aid ' +\
                 'where g.name like %s ' +\
                 'group by a.aid;', ['%' + query + '%'])
    
    return curs.fetchall()
    

def searchTrack(query, conn):
    '''returns all albums that contain
    the query in their track list'''

    curs = dbi.dictCursor(conn)
    curs.execute('select * from album a ' +\
                 'inner join track t ' +\
                    'on a.aid = t.aid ' +\
                 'where t.name like %s ' +\
                 'group by a.aid;', ['%' + query + '%'])

    return curs.fetchall()

def getAlbumByID(aid, conn):
    '''returns an album with that id'''
    curs = dbi.dictCursor(conn)
    curs.execute('select * from album where aid = %s', [aid])
    return curs.fetchone()
    
def getReservation(aid, conn):
    '''gets the most recent reservation
    for a particular album id'''
    curs = dbi.dictCursor(conn)
    curs.execute('select * from reservation where aid = %s ' +\
                  'order by due desc limit 1;', [aid])
    
    return curs.fetchone()

def getGenres(aid, conn):
    '''gets genres for an album
    given album's id'''
    curs = dbi.dictCursor(conn)
    curs.execute('select * from genre where aid = %s', [aid])
    
    return curs.fetchall()

def getTracks(aid, conn):
    ''''gets tracks for an album
    given album's id'''
    curs = dbi.dictCursor(conn)
    curs.execute('select * from track where aid = %s', [aid])
    
    return curs.fetchall()

# use this code to update all rows where this happens
def fixThe():
    conn = getConn('cs304reclib_db')
    curs = dbi.dictCursor(conn)
    curs.execute("select * from track where name like '%, the%'")
    albums = curs.fetchall()

    for a in albums:
        print(a['name'])
    
    # name = album['name']
    # artist = album['artist']

    # if ', the' in artist.lower():
    #     i = artist.lower().index(', the')
    #     album['artist'] = 'The ' + artist[:i]
    # if ',the' in artist.lower():
    #     i = artist.lower().index(',the')
    #     album['artist'] = 'The ' + artist[:i]
    # if ', the' in name.lower():
    #     i = name.lower().index(', the')
    #     album['name'] = 'The ' + name[:i]
    # if ',the' in name.lower():
    #     i = name.lower().index(',the')
    #     album['name'] = 'The ' + name[:i]
    
    # return album

# conn = getConn('cs304reclib_db')
# album = getAlbumByID(3045, conn)
# print(fixThe(album))

fixThe()