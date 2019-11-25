import csv
import dbi
from spotify import *

def addAlbums(conn):
    # reads results.csv and updates appropriate tables

    with open('./results.csv') as csv_read:
        
        reader = csv.reader(csv_read, delimiter=',')

        linecount = 0

        for row in reader:
            if linecount == 0:
                linecount += 1
            else:
                print('processing ', linecount, ' lines')
                linecount += 1

                if len(row) > 3:
                    for i in range(len(row) - 1):
                        if row[i] == '':
                            row[i] = None

                    tracks = tracklist(row[9])
                    genres = genrelist(row[8])

                    aid = insertAlbum(row, conn)
                    insertTracks(tracks, aid, conn)
                    insertGenres(genres, aid, conn)
                else:
                    lowData(row, conn)
                    
        return

def getConn(db):
    '''Returns a database connection for that db'''
    dsn = dbi.read_cnf()
    conn = dbi.connect(dsn)
    conn.select_db(db)
    return conn

def tracklist(tracks):
    '''given a list of tracks in string form,
    processes them and returns a list
    of lists containing the track name, order, and id'''

    try:
        tracks = tracks[1:-1]

        tracks = tracks.split('], [')
        tx = []

        for t in tracks:
            t = t + ']'
            t = t.strip('][')
            t = t.replace("'", '')
            t = t.split(', ')
            try:
                t[1] = int(t[1])
            except:
                for i in range(len(t) - 1):
                    if (t[i].isdigit()):
                        t[0:i] = [', '.join(t[0:i])]
                        t[1] = int(t[1])
            tx.append(t)
    
        return tx
    except:
        return ''

def genrelist(genres):
    
    try:
        genres = genres.strip('][').replace("'", '').split(', ')
        return genres
    except:
        return ''

def insertTracks(tracklist, aid, conn):
    '''adds tracks and their order
    to track table'''

    curs = dbi.dictCursor(conn)
    for track in tracklist:
        curs.execute('insert into track ' +\
                     '(name, num, spotify_id, aid) ' +\
                     'values (%s, %s, %s, %s)',
                     [track[0], track[1], track[2], aid])

def insertGenres(genrelist, aid, conn):
    '''adds genres and their corresponding
    album to the genres table'''

    curs = dbi.dictCursor(conn)
    for genre in genrelist:
        curs.execute('insert into genre (name, aid) ' +\
                     'values (%s, %s)', [genre, aid])

def insertAlbum(row, conn):
    album = row[0]
    artist = row[1]
    location = row[2]
    spotify_artist_id = row[3]
    spotify_album_id = row[4]
    released = int(row[5])
    art = row[6]
    embed = row[7]
    spotify_name = getAlbumName(embed)
    spotify_artist = getArtistName(embed)

    curs = dbi.dictCursor(conn)
    curs.execute('insert into album ' +\
                    '(name, artist, fmt, ' +\
                    'spotify_name, spotify_artist, location, ' +\
                    'year, art, embed, spotify_album_id, ' +\
                    'spotify_artist_id)'
                    'values ' +\
                    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                    [album, artist, 'cd', spotify_name, spotify_artist,
                    location, released, art, embed,
                    spotify_album_id, spotify_artist_id])

    curs.execute('select LAST_INSERT_ID();')
    aid = curs.fetchone()['LAST_INSERT_ID()']
    
    return aid
    

def lowData(row, conn):
    album = row[0]
    artist = row[1]
    location = row[2]

    curs = dbi.dictCursor(conn)
    curs.execute('insert into album ' +\
                    '(name, artist, fmt, ' +\
                    'spotify_name, spotify_artist, location, ' +\
                    'year, art, embed, spotify_album_id, ' +\
                    'spotify_artist_id)'
                'values ' +\
                    '(%s, %s, %s, NULL, NULL, ' +\
                    '%s, NULL, NULL, NULL, NULL, NULL);',
                    [album, artist, 'cd', location])

    curs.execute('select LAST_INSERT_ID();')
    aid = curs.fetchone()['LAST_INSERT_ID()']
    
    return aid

# conn = getConn('cs304reclib_db')
# addAlbums(conn)

def updateThe(column, conn):
    '''Addresses format variations including "the"
    ex. changes "Beatles, The" to "The Beatles"'''
    curs = dbi.dictCursor(conn)
    
    if column == 'name':
        curs.execute("select name, aid from album where name like '%the'")
    if column == 'artist':
        curs.execute("select artist, aid from album where artist like '%the'")
    else:
        print("Please select a valid column")
        return

    fixes = curs.fetchall()
    count = 0

    # iterate through all albums where a value ends with 'the'
    for album in fixes:
        print("processing " + str(count) + " of " + str(len(fixes)))
        print(album)
        
        fix = album[column]
        aid = album['aid']

        # check for both formats
        fix = fixThes(fix, ', the')
        fix = fixThes(fix, ',the')
        print(fix)
        
        if column == 'name':
            curs.execute("update album set name = %s where aid = %s", [fix, aid])
        if column == 'artist':
            curs.execute("update album set artist = %s where aid = %s", [fix, aid])
        
        count += 1

def fixThes(name, phrase):
    
    if phrase in name.lower():
        i = name.lower().rfind(phrase)
        # the phrase is the last part of the name
        if i == (len(name) - len(phrase)):
            name = 'The ' + name[:i]
    
    return name

def manualFixes(conn):
    curs = dbi.dictCursor(conn)

    curs.execute('update album set artist = %s where aid = %s',
                 ['The Wee Turtles', 951])
    curs.execute('update album set artist = %s where aid = %s',
                 ['The Popinjays', 2399])
    curs.execute('update album set artist = %s where aid = %s',
                 ['The Popinjays', 2397])
    curs.execute('update album set artist = %s where aid = %s',
                 ['The Third Sex', 13343])
    curs.execute('update album set artist = %s where aid = %s',
                 ['The Honeydogs', 15218])