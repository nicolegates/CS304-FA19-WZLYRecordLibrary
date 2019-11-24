use cs304reclib_db;

DROP TABLE IF EXISTS track;

CREATE TABLE track (
    name varchar(150),
    num int,
    spotify_id varchar(22),
    tid int NOT NULL AUTO_INCREMENT,
    aid int NOT NULL,
    primary key (tid),
    foreign key (aid)
        references album(aid)
        on delete cascade
)