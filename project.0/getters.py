import dbi

def getConn(db):
    '''Returns a database connection for that db'''
    dsn = dbi.read_cnf()
    conn = dbi.connect(dsn)
    conn.select_db(db)
    return conn

# TODO: WRITE THESE!!!!!
def getAlbums(query, conn):
    '''adds tracks and their order
    to track table'''

    curs = dbi.dictCursor(conn)
    curs.execute('insert into track ' +\
                     '(name, num, spotify_id, aid) ' +\
                     'values (%s, %s, %s, %s)',
                     [track[0], track[1], track[2], aid])

    return curs.fetchall()

def getArtists(query, conn):
    '''returns all artists matching a query'''

    curs = dbi.dictCursor(conn)
    curs.execute('select * from album ' +\
                 'where artist like %s',
                  ['%' + query + '%'])
    return curs.fetchall()

def getYear(query, conn):
    '''returns all albums from given year'''

    curs = dbi.dictCursor(conn)
    curs.execute('select * from album ' +\
                 'where year = %s',
                  [query])
    return curs.fetchall()

def getGenre(query, conn):
    '''returns all albums of a specific genre'''

    curs = dbi.dictCursor(conn)
    curs.execute('select * from album a ' +\
                 'inner join genre g ' +\
                    'on a.aid = g.aid ' +\
                 'where g.name like %s ' +\
                 'group by a.aid;', ['%' + query + '%'])
    
    return curs.fetchall()
    

def getTrack(query, conn):
    '''returns all albums that contain
    the query in their track list'''

    curs = dbi.dictCursor(conn)
    curs.execute('select * from album a ' +\
                 'inner join track t ' +\
                    'on a.aid = t.aid ' +\
                 'where t.name like %s ' +\
                 'group by a.aid;', ['%' + query + '%'])
    
    return curs.fetchall()

conn = getConn('cs304reclib_db')
res = getTrack('lotus', conn)
print(res)
print(len(res))