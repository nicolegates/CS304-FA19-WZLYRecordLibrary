import dbi

def getConn(db):
    '''Returns a database connection for that db'''
    dsn = dbi.read_cnf()
    conn = dbi.connect(dsn)
    conn.select_db(db)
    return conn

def searchAlbums(query, conn):
    '''returns all albums matching a query'''

    curs = dbi.dictCursor(conn)
    curs.execute('select * from album where name like %s',
                ['%' + query + '%'])

    return curs.fetchall()

def searchArtists(query, conn):
    '''returns all artists matching a query'''

    curs = dbi.dictCursor(conn)
    curs.execute('''select * from album
                    where artist like %s''',
                    ['%' + query + '%'])
    return curs.fetchall()

def searchYear(query, conn):
    '''returns all albums from given year'''

    curs = dbi.dictCursor(conn)
    curs.execute('''select * from album
                    where year = %s''',
                  [query])
    return curs.fetchall()

def searchGenre(query, conn):
    '''returns all albums of a specific genre'''

    curs = dbi.dictCursor(conn)
    curs.execute('''select * from album a
                    inner join genre g
                        on a.aid = g.aid
                    where g.name like %s
                    group by a.aid;''',
                    ['%' + query + '%'])
    
    return curs.fetchall()
    

def searchTrack(query, conn):
    '''returns all albums that contain
    the query in their track list'''

    curs = dbi.dictCursor(conn)
    curs.execute('''select * from album a
                    inner join track t
                        on a.aid = t.aid
                    where t.name like %s
                    group by a.aid;''',
                    ['%' + query + '%'])

    return curs.fetchall()

def getAlbumByID(aid, conn):
    '''returns a dictionary representation
    of an album matching provided id'''
    curs = dbi.dictCursor(conn)
    curs.execute('select * from album where aid = %s', [aid])
    return curs.fetchone()

def getRandomAlbums(conn):
    '''returns 5 random albums to display on front page'''
    curs = dbi.dictCursor(conn)
    curs.execute('select * from album order by RAND() limit 5')
    return curs.fetchall()
    
def getReservation(aid, conn):
    '''gets the most recent reservation
    for a particular album id'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from reservation where aid = %s
                    order by due desc limit 1;''', [aid])
    
    return curs.fetchone()

def getReservations(filter, conn):
    '''returns reservations according to selected filter'''

    curs = dbi.dictCursor(conn)

    if filter == 'all':
        curs.execute('''select
                        reservation.*, person.name,
                        album.name as album_name, album.artist
                     from reservation
                        inner join person
                            on reservation.bid = person.bid
                        inner join album
                            on reservation.aid = album.aid;''')

    if filter == 'overdue':
        curs.execute('''select
                        reservation.*, person.name,
                        album.name as album_name, album.artist
                     from reservation
                        inner join person
                            on reservation.bid = person.bid
                        inner join album
                            on reservation.aid = album.aid
                     where reservation.due <= CURDATE()
                        and reservation.returned = 0;''')
    
    return curs.fetchall()

def getGenres(aid, conn):
    '''returns a list of dictionaries
    containing the name of the genre and
    the album's ID'''
    curs = dbi.dictCursor(conn)
    curs.execute('select * from genre where aid = %s', [aid])
    
    return curs.fetchall()

def getTracks(aid, conn):
    ''''gets tracks for an album
    given album's id'''
    curs = dbi.dictCursor(conn)
    curs.execute('select * from track where aid = %s', [aid])
    
    return curs.fetchall()

def getArtist(artist, conn):
    '''gets all an artist's albums'''
    curs = dbi.dictCursor(conn)
    curs.execute('select * from album where artist = %s;', [artist])

    return curs.fetchall()

def getIncompletes(conn):
    '''returns all albums with incomplete info'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from album where
                    year IS NULL''')
    incompletes = curs.fetchall()
    return incompletes

def getActiveReservationsByID(bid, conn):
    '''returns all active reservations for a particular user'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select
                        reservation.*, person.name,
                        album.name as album_name, album.artist
                    from reservation
                        inner join person
                            on reservation.bid = person.bid
                        inner join album
                            on reservation.aid = album.aid
                    where person.bid = %s
                        and reservation.returned = 0;''', [bid])
    res = curs.fetchall()
    return res

def getOverdueReservationsByID(bid, conn):
    '''returns all overdue reservations for a particular user'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select
                        reservation.*, person.name,
                        album.name as album_name, album.artist
                    from reservation
                        inner join person
                            on reservation.bid = person.bid
                        inner join album
                            on reservation.aid = album.aid
                    where person.bid = %s
                        and reservation.returned = 0
                        and reservation.due <= CURDATE()''', [bid])
    res = curs.fetchall()
    return res

def getAllReservationsByID(bid, conn):
    '''returns all reservations ever made by a particular user'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from reservation where
                    bid = %s''', [bid])
    res = curs.fetchall()
    return res

def getOverdueEmails(conn):
    '''returns all usernames who have overdue items'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select username
                        from person
                    inner join reservation
                        on reservation.bid = person.bid
                    where reservation.due <= CURDATE()
                    and reservation.returned = 0;''')
    return curs.fetchall()

def getBIDFromUsername(conn, username):
    '''get bid from username'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select bid from person where
                    username = %s''', [username])
    return curs.fetchone()
    
def getAdmins(conn):
    '''get all admins'''
    curs = dbi.dictCursor(conn)
    curs.execute("select username from person where is_admin = 1")
    return curs.fetchall()

def isAdmin(username, conn):
    '''checks if user is an admin'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select is_admin
                    from person where username = %s''',
                [username])
    if curs.fetchone()['is_admin'] == 1:
        return True
    else:
        return False

def getGenreList(conn):
    '''gets all genres'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select distinct `name` from genre
                    order by `name`''')
    return curs.fetchall()

def getUserGenres(conn, bid):
    '''gets users top genres'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select genre1, genre2, genre3 from person
                    where bid=%s''', [bid])
    return curs.fetchone()

def getRecommendedAlbums(conn, genre1, genre2, genre3):
    '''gets random albums from the users top genres'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from album 
                    inner join genre
                    on album.aid = genre.aid
                    where genre.name = %s or genre.name = %s or genre.name = %s
                    order by RAND() 
                    limit 5''', (genre1, genre2, genre3))
    return curs.fetchall()