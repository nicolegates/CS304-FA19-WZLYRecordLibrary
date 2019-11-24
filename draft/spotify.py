from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

client = os.getenv('client_id')
secret = os.getenv('secret')

client_credentials_manager = SpotifyClientCredentials(client_id=client, client_secret=secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getAlbum(artist, album):
    query='artist:' + artist + ' album:' + album
    results = spotify.search(q=query, type='album')
    if len(results['albums']['items']) > 0:
        return results['albums']['items'][0]
    else:
        return False

def getProps(album):
    spotify_album_id = album['id']
    tracks = getTracks(spotify_album_id)
    spotify_artist_id = album['artists'][0]['id']
    released = album['release_date']
    if (album['release_date_precision'] != 'year'):
        released = album['release_date'][0:4]
    if len(album['images']) > 0:
        art = album['images'][0]['url']
    else:
        art = ''
    embed = album['uri']
    genres = getGenres(spotify_artist_id)

    return { 'spotify_album_id': spotify_album_id,
             'spotify_artist_id': spotify_artist_id,
             'released': released,
             'art': art,
             'embed': embed,
             'genres': genres,
             'tracks': tracks }

def getGenres(artist_id):
    artist = spotify.artist(artist_id)
    return artist['genres']

def getTracks(album_id):
    tracks = spotify.album_tracks(album_id=album_id)
    
    tracklist = []
    for t in tracks['items']:
        trk = [t['name'], t['track_number'], album_id]
        tracklist.append(trk)

    return tracklist

def getArtistName(album_id):
    try:
        return spotify.album(album_id)['artists'][0]['name']
    except:
        return None

def getAlbumName(album_id):
    try:
        return spotify.album(album_id)['name']
    except:
        return None
    
    

# spotify embed code
# <iframe src="https://open.spotify.com/embed/album/1XslIirSxfAhhxRdn4Li9t" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>

album = getAlbumName('spotify:album:48VaRUNrCOe2mm6v6FnapS')
artist = getArtistName('spotify:album:48VaRUNrCOe2mm6v6FnapS')
print(album)
print(artist)