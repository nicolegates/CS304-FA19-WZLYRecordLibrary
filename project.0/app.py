# taken from hwk5, needs to be updated

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import sys,os,random
import crud
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
    conn = getters.getConn('wmdb')
    args = request.args

    if 'q' in args:
        q = args['q']
    if 'filter' in args:
        kind = args['filter']

    print(q)
    print(kind)

    if kind == 'album':
        results = getters.getAlbums(q, conn)
    if kind == 'artist':
        results = getters.getArtists(q, conn)
    if kind == 'year':
        results = getters.getYear(q, conn)
    if kind == 'genre':
        results = getters.getGenre(q, conn)
    if kind == 'track':
        results = getters.getTrack(q, conn)

    return render_template('results.html',
                            results=people,
                            query=q,
                            kind='People')

#     if (kind == 'person'):
#         people = getters.getPeople(q, conn)
#         if len(people) == 1:
#             person = people[0]
#             nm = person['nm']
#             return redirect(url_for('get_person', nm=nm))
#         if people is None or len(people)==0:
#             return render_template('error.html',
#                                     msg='Sorry, no people found')
#         else:
#             return render_template('results.html',
#                                     results=people,
#                                     query=q,
#                                     kind='People')
#     if (kind == 'movie'):
#         movies = getters.getMovies(q, conn)
#         if len(movies) == 1:
#             movie = movies[0]
#             tt = movie['tt']
#             return redirect(url_for('get_movie', tt=tt))
#         if movies is None or len(movies)==0:
#             return render_template('error.html',
#                                     msg='Sorry, no movies found')
#         else:
#             return render_template('results.html',
#                                     results=movies,
#                                     query=q,
#                                     kind='Movies')     
        

# @app.route('/insert/', methods=['GET','POST'])
# def insert():
#     conn = crud.getConn('ivirgili_db')
#     movies = crud.getIncompletes(conn)
    
#     if request.method == 'POST':
#         tt = request.form.get('movie-tt')
#         title = request.form.get('movie-title')
#         year = request.form.get('movie-release')

#         # if a field is empty/not filled
#         # out correctly
#         error = False
#         if not tt.isdigit():
#             flash('TT is not numeric.')
#             error = True
#         if len(tt) > 10:
#             flash('TT may be no more than 10 integers long.')
#             error = True
#         if not title:
#             flash('Missing input: Title is missing')
#             error = True
#         if not year:
#             flash('Missing input: Release year is missing')
#             error = True
        
#         if error:
#             return render_template('insert.html')

#         # check if the movie already exists
#         movie = crud.getMovieInfo(tt, conn)

#         if movie != None:
#             flash('Error: Movie with tt=' +\
#                    tt + ' already in database.')
#         # if it's not in the database, insert it
#         else:
#             crud.insertMovie(tt, title, year, conn)

#         return redirect(url_for('update', 
#                                 tt = tt))
    
#     return render_template('insert.html')
    
# @app.route('/select/', methods=['GET','POST'])
# def select():
#     conn = crud.getConn('ivirgili_db')
    
#     # get movies with incomplete fields
#     movies = crud.getIncompletes(conn)
    
#     if request.method == 'POST':
#         tt = request.form.get('menu-tt')

#         return redirect(url_for('update', 
#                                 tt = tt))
    
#     return render_template('select.html', movies = movies)
            
# @app.route('/update/<tt>', methods=['GET','POST'])
# def update(tt):
#     conn = crud.getConn('ivirgili_db')
#     info = crud.getMovieInfo(tt,conn)
#     director = crud.getDirector(info['director'], conn)

#     if director != None:
#         director = director['name']

#     if request.method == 'GET':
#         return render_template('update.html', tt = tt, \
#                             title = info['title'],
#                             year = info['release'],
#                             did = info['director'],
#                             director = director,
#                             id = info['addedby'])

#     if request.method == 'POST':
#         form = request.form

#         # get user input from the form
#         action = form['submit']
#         new_tt = form['movie-tt']
#         name = form['movie-title']
#         year = form['movie-release']
#         addedby = form['movie-addedby']
#         did = form['movie-director']

#         if action == 'update':
#             # if the user enters some variation of "null" or "none"
#             if (did.lower() == "null" or did.lower() == "none"):
#                 did = None
#                 director = 'None Specified'
#             # if the user enters an ID
#             else:
#                 d = crud.getDirector(did, conn)
#                 # if the ID exists in the person table,
#                 # get the director's name
#                 if d != None:
#                     director = d['name']
#                 # if the ID does not exist
#                 else:
#                     flash("Director does not exist.")
#                     return render_template('update.html',
#                                             tt = tt, \
#                                             title = info['title'],
#                                             year = info['release'],
#                                             did = "None",
#                                             director = "None",
#                                             id = info['addedby'])

#             # update the movie in the movie table
#             result = crud.updateMovie(tt,
#                                       new_tt,
#                                       name,
#                                       year,
#                                       addedby,
#                                       did,
#                                       conn)
            
#             # if the movie was updated successfully
#             if result == True:
#                 flash("Movie (" + name + ") was updated successfully")
#                 return render_template('update.html', tt = new_tt, \
#                             title = name,
#                             year = year,
#                             did = did,
#                             director = director,
#                             id = addedby)
            
#             # if the movie is already in the table
#             if result == False:
#                 flash("Movie already exists.")
#                 return render_template('update.html', tt = tt, \
#                                                       title = info['title'],
#                                                       year = info['release'],
#                                                       did = info['director'],
#                                                       director = director,
#                                                       id = info['addedby'])
#         if action == 'delete':
#             crud.deleteMovie(tt, conn)
#             flash("Movie (" + name + ") was deleted")
#             return render_template('base.html')

if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)