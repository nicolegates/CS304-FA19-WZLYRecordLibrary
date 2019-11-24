from dotenv import load_dotenv
from spotify import *
import csv
from itertools import islice

def read():
    with open('./source.csv') as csv_read:
        reader = csv.reader(csv_read, delimiter=',')

        for row in islice(reader, 14097, None):
            print(row)
            return

def write(start):

    with open('./source.csv') as csv_read, \
         open('./results.csv', 'a') as csv_write:
        
        reader = csv.reader(csv_read, delimiter=',')
        writer = csv.writer(csv_write, delimiter=',')

        line_count = 0            

        for row in islice(reader, start, None):

            if line_count == 0:
                line_count += 1
            else:
                artist = row[1]
                album = row[0]
                location = row[2]

                if location.lower() != 'trash':
                    record = getAlbum(artist, album)

                    if not record:
                        writer.writerow(row)
                    else:
                        props = getProps(record)

                        row.append(props['spotify_artist_id'])
                        row.append(props['spotify_album_id'])
                        row.append(props['released'])
                        row.append(props['art'])
                        row.append(props['embed'])
                        row.append(props['genres'])
                        row.append(props['tracks'])
                        writer.writerow(row)
                        print(f'Processed {line_count} lines.')

            line_count += 1