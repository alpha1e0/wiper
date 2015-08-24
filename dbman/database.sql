drop database wip;
create database wip;
use wip;


create table project (
	id integer not null auto_increment, 
	name varchar(100) not null unique,
	url varchar(100), 
	ip varchar(50), 
	whois text, 
	ctime timestamp not null default CURRENT_TIMESTAMP,
	description text,
	primary key (id)
) engine=InnoDB  default charset=utf8;

create table host (
	id integer not null auto_increment, 
	url varchar(100), 
	ip varchar(50), 
	level integer, 
	os varchar(150), 
	server_info varchar(150),
	middleware varchar(200), 
	description text, 
	project_id integer not null, 
	primary key (id),
	constraint project_id_host foreign key (project_id) references project (id)
) engine=InnoDB  default charset=utf8;


create table vul (
	id integer not null auto_increment, 
	name varchar(50), 
	url varchar(4096),
	info varchar(1024), 
	type integer, 
	level integer, 
	description text, 
	host_id integer not null, 
	primary key (id),
	constraint host_id_vul foreign key (host_id) references host (id)
) engine=InnoDB  default charset=utf8;


create table comment (
	id integer not null auto_increment, 
	name varchar(100), 
	url varchar(4096),
	info varchar(1024), 
	level integer, 
	attachment varchar(100),
	description text, 
	host_id integer not null, 
	primary key (id),
	constraint host_id_comment foreign key (host_id) references host (id)
) engine=InnoDB  default charset=utf8;


create table tmp_task_result_byhost (
	id integer not null auto_increment, 
	url varchar(100), 
	ip varchar(50), 
	level integer,
	source varchar(50),
	project_id integer not null,
	primary key (id),
	constraint project_id_host foreign key (project_id) references project (id)
) engine=InnoDB  default charset=utf8;
