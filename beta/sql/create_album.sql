use cs304reclib_db;

DROP TABLE IF EXISTS album;

CREATE TABLE album (
    aid int NOT NULL AUTO_INCREMENT,
    name varchar(150) NOT NULL,
    artist varchar(150) NOT NULL,
    fmt ENUM('cd', 'record'), -- all entries will be CDs, but records will be added later
    spotify_name varchar(150), -- a more 'accurate' album title
    spotify_artist varchar(150), -- a more 'accurate' artist name
    location varchar(50), -- this will be null for most records
    year int,
    art varchar(2083),
    embed varchar(2083),
    spotify_album_id varchar(22),
    spotify_artist_id varchar(22),
    primary key (aid)
)