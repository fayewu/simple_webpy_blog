use web_test;

create table sessions (
	session_id char(128) unique not null,
	atime timestamp not null default current_timestamp,
	data text
);
