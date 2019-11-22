use cs304reclib_db;

DROP TABLE IF EXISTS genre;

CREATE TABLE genre (
    name varchar(150),
    aid int NOT NULL,
    foreign key (aid)
        references album(aid)
        on delete cascade
)