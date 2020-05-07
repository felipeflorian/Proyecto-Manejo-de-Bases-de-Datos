create table Solicitud
 (id serial,
  solicitud varchar,
  solicitante varchar,
  estado varchar,
  fecha varchar,
  primary key(id));

create table Camara
(numero serial,
 tipo_equipo varchar,
 latitud varchar,
 longitud varchar,
 direccion varchar,
 estado_solicitud varchar,
 solicitud varchar,
 foreign key(numero) references Solicitud);
