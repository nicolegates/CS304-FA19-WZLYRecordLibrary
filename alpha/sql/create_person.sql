use cs304reclib_db;

DROP TABLE IF EXISTS person;

CREATE TABLE person (
    bid varchar(9) NOT NULL,
    name varchar(150) NOT NULL,
    username varchar(8) NOT NULL,
    genre1 varchar(50),
    genre2 varchar(50),
    genre3 varchar(50),
    is_admin BOOLEAN NOT NULL,
    primary key (bid)
)