-- create table Solicitud
--  (id serial,
--   solicitud varchar not null,
--   solicitante varchar not null,
--   fecha_hora varchar not null,
--   primary key(id));

create table Equipo
(id serial,
 tipo_equipo varchar not null,
 latitud varchar not null,
 longitud varchar not null,
 direccion varchar not null,
 departamento varchar not null,
 municipio varchar not null,
 primary key(id));

create table tipoMulta
(codigo_multa varchar not null,
 tipo_multa varchar not null,
 primary key(codigo_multa));

create table Multa
(id serial,
 codigo_multa varchar not null,
 latitud varchar not null,
 longitud varchar not null,
 foreign key(codigo_multa) references tipoMulta);
