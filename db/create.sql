create database web_test;
use web_test;

create table user (
	username varchar(100) primary key,
	passwd varchar(100) not NULL
);
insert into user(username, passwd) values("test", "test"); 
