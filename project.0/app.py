from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import sys,os,random
import getters

from dotenv import load_dotenv
load_dotenv()

app.secret_key = os.getenv('secret_key')
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/query', methods=['GET','POST'])
def query():
    conn = getters.getConn('cs304reclib_db')
    args = request.args

    if 'q' in args:
        q = args['q']
    if 'filter' in args:
        kind = args['filter']

    if kind == 'album':
        results = getters.searchAlbums(q, conn)
    if kind == 'artist':
        results = getters.searchArtists(q, conn)
    if kind == 'year':
        results = getters.searchYear(q, conn)
    if kind == 'genre':
        results = getters.searchGenre(q, conn)
    if kind == 'track':
        results = getters.searchTrack(q, conn)

    return render_template('results.html',
                            results=results,
                            query=q,
                            kind=kind)

@app.route('/album/<aid>')
def album(aid):
    conn = getters.getConn('cs304reclib_db')
    album = getters.getAlbumByID(aid, conn)
    
    res = getters.getReservation(aid, conn)
    tracks = getters.getTracks(aid, conn)
    genres = getters.getGenres(aid, conn)
    
    # if the album has been returned
    if res is None or res['returned'] == 1:
        avail = 'Available'
    # if not, pass the due date to the template
    else:
        avail = 'Due back ' + res['due'].strftime('%m/%d/%Y')

    print(album['location'])

    return render_template('album.html',
                            album=album,
                            avail=avail,
                            tracks=tracks,
                            genres=genres)

@app.route('/login/')
def login():
    return redirect(url_for('index'))

@app.route('/profile/')
def profile():
    return redirect(url_for('index'))

@app.route('/checkin/')
def checkin():
    return redirect(url_for('index'))

@app.route('/admin/')
def admin():
    return redirect(url_for('index'))

if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)