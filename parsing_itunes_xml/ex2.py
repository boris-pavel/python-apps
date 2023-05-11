import sqlite3
import xml.etree.ElementTree as ET

library = ET.parse(open('Library.xml'))
conn = sqlite3.connect('ex2.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Artist;
''')
cur.execute('''
DROP TABLE IF EXISTS Genre;
''')
cur.execute('''
DROP TABLE IF EXISTS Album;
''')
cur.execute('''
DROP TABLE IF EXISTS Track;
''')

cur.execute('''
CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
''')

cur.execute('''
CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
''')

cur.execute('''
CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);
''')

cur.execute('''
CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

data = library.findall('dict/dict/dict')


def look_up(d, key):
    found = False
    for child in d:
        if found:
            return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None


for entry in data:
    name = look_up(entry, 'Artist')
    genre = look_up(entry, 'Genre')
    album_title = look_up(entry, 'Album')
    track_title = look_up(entry, 'Name')
    length = look_up(entry, 'Total Time')
    rating = look_up(entry, 'Rating')
    count = look_up(entry, 'Play Count')

    if name is None or genre is None or album_title is None:
        continue

    cur.execute('''
    INSERT OR IGNORE INTO Artist (name) VALUES (?)
    ''', (name,))
    cur.execute('''
    SELECT id FROM Artist WHERE name = ?
    ''', (name,))
    artist_id = cur.fetchone()[0]

    cur.execute('''
    INSERT OR IGNORE INTO Genre (name) VALUES (?)
    ''', (genre,))
    cur.execute('''
    SELECT id FROM Genre WHERE name = ?
    ''', (genre,))
    genre_id = cur.fetchone()[0]

    cur.execute('''
    INSERT OR REPLACE INTO Album (artist_id, title) VALUES (?,?)
    ''', (artist_id, album_title))
    cur.execute('''
    SELECT id FROM Album WHERE title = ?
    ''', (album_title,))
    album_id = cur.fetchone()[0]

    cur.execute('''
    INSERT OR REPLACE INTO Track 
    (title, album_id, genre_id, len, rating, count)
    VALUES
    (?,?,?,?,?,?)
    ''',(track_title, album_id, genre_id, length, rating, count))


    conn.commit()
