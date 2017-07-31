drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);
/*This schema consists of a single table called entries. Each row in this
table has an id, a title, and a text. The id is an automatically incrementing
integer and a primary key, the other two are strings that must not be null.*/
