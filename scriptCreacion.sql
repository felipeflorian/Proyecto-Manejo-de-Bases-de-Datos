create table Equipo
(id1 serial,
 tipo_equipo varchar not null,
 latitud varchar not null,
 longitud varchar not null,
 direccion varchar not null,
 departamento varchar not null,
 municipio varchar not null,
 primary key(id1));


create table tipoMulta
(codigo_multa varchar not null,
 tipo_multa varchar not null,
 monto integer not null,
 primary key(codigo_multa));

create table Multa
(id serial,
 edad varchar not null,
 placa varchar not null,
 fecha varchar not null,
 codigo_multa varchar not null,
 latitud varchar not null,
 longitud varchar not null,
 foreign key(codigo_multa) references tipoMulta);

create or replace function multasMenoresDe(edad1 varchar)
RETURNS TABLE (codMulta varchar, numero_multas bigint, e varchar) as $$
BEGIN
  RETURN QUERY select
    codigo_multa,
    count(edad),
    edad
  from
    multa
  where
    edad < edad1
  group by edad, codigo_multa;
END;
$$ LANGUAGE plpgsql;

create or replace function multasMayoresDe(edad1 varchar)
RETURNS TABLE (codMulta varchar, numero_multas bigint, e varchar) as $$
BEGIN
  RETURN QUERY select
    codigo_multa,
    count(edad),
    edad
  from
    multa
  where
    edad > edad1
  group by edad, codigo_multa;
END;
$$ LANGUAGE plpgsql;

create or replace function busquedaPorPlac(pla varchar)
RETURNS TABLE (placa varchar, codigo_multa varchar, dir varchar) as $$
BEGIN
  RETURN QUERY
  SELECT multa.placa, tipomulta.codigo_multa, equipo.direccion
  FROM multa JOIN tipoMulta ON multa.codigo_multa = tipoMulta.codigo_multa
           JOIN equipo ON equipo.latitud = multa.latitud
  where multa.placa = 'SZF883';
END;
$$ LANGUAGE plpgsql;

create or replace function montoTotalMultas(cod varchar)
RETURNS INTEGER  as $$
BEGIN
  RETURN  count(multa.codigo_multa)*monto
  from multa join tipomulta on multa.codigo_multa = tipomulta.codigo_multa
  where multa.codigo_multa = 'D06'
  group by tipomulta.monto;
END;
$$ LANGUAGE plpgsql;

--monto antes de una fecha
