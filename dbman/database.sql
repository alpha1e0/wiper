drop database wip;
create database wip;
use wip;


create table project (
	id integer not null auto_increment, 
	name varchar(100) unique,
	url varchar(100), 
	ip varchar(50), 
	whois text, 
	description text,
	primary key (id)
) engine=InnoDB  default charset=utf8;

create table host (
	id integer not null auto_increment, 
	url varchar(100), 
	ip varchar(50), 
	level integer, 
	os varchar(150), 
	web_server varchar(150),
	web_framework varchar(200), 
	description text, 
	project_id integer not null, 
	primary key (id),
	constraint project_id_host foreign key (project_id) references project (id)
) engine=InnoDB  default charset=utf8;

create table port (
	id integer not null auto_increment, 
	port int, 
	app varchar(100), 
	version varchar(100), 
	level integer, 
	description text, 
	host_id integer not null, 
	primary key (id),
	constraint host_idc_port foreign key (host_id) references host (id)
) engine=InnoDB  default charset=utf8;

create table vul (
	id integer not null auto_increment, 
	name varchar(50), 
	info varchar(1024), 
	type integer, 
	levle integer, 
	description text, 
	host_id integer not null, 
	port_id integer not null, 
	primary key (id),
	constraint host_id_vul foreign key (host_id) references host (id), 
	constraint port_id_vul foreign key (port_id) references port (id)
) engine=InnoDB  default charset=utf8;



create table comment (
	id integer not null auto_increment, 
	name varchar(100), 
	info varchar(1024), 
	level integer, 
	attachment varchar(100),
	description text, 
	host_id integer not null, 
	port_id integer not null, 
	primary key (id),
	constraint host_id_comment foreign key (host_id) references host (id), 
	constraint port_id_comment foreign key (port_id) references port (id)
) engine=InnoDB  default charset=utf8;

