create table usuario (
	cod_usuario bigint primary key,
	nome_usuario varchar(255),
	capsulas int
);

create table chave (
	horario timestamp primary key,
	local varchar(255),
	cod_usuario int references usuario on delete cascade on update cascade
);

create table sala (
	status int primary key
);

insert into usuario(cod_usuario, nome_usuario, capsulas) values(0, 'Secretaria', 0);
insert into sala values(0);
