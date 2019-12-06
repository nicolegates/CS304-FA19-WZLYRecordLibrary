use cs304reclib_db;

DROP TABLE IF EXISTS reservation;

CREATE TABLE reservation (
  rid int NOT NULL AUTO_INCREMENT,
  checkout date,
  due date,
  returned BOOLEAN NOT NULL,
  aid int NOT NULL,
  bid varchar(9) NOT NULL,
  primary key (rid),
  foreign key (aid)
    references album(aid)
    on delete cascade,
  foreign key (bid)
    references person(bid)
    on delete cascade
)