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
 estado varchar,
 primary key(id),
 foreign key(codigo_multa) references tipoMulta);

create or replace function multasMenoresDe(edad1 varchar)
RETURNS TABLE (codMulta varchar, cantidad_multas bigint, edad varchar) as $$
BEGIN
  RETURN QUERY select
    multa.codigo_multa,
    count(multa.edad),
    multa.edad
  from
    multa
  where
    multa.edad < edad1
  group by multa.edad, multa.codigo_multa;
END;
$$ LANGUAGE plpgsql;

create or replace function multasMayoresDe(edad1 varchar)
RETURNS TABLE (codMulta varchar, cantidad_multas bigint, edad varchar) as $$
BEGIN
  RETURN QUERY select
    multa.codigo_multa,
    count(multa.edad),
    multa.edad
  from
    multa
  where
    multa.edad > edad1
  group by multa.edad, multa.codigo_multa;
END;
$$ LANGUAGE plpgsql;

create or replace function busquedaPorPlaca(pla varchar)
RETURNS TABLE (Estado varchar, Placa varchar, Codigo_multa varchar, tipo_multa varchar, monto integer) as $$
BEGIN
  RETURN QUERY
  SELECT multa.estado, multa.placa, tipomulta.codigo_multa, tipomulta.tipo_multa, tipomulta.monto
  from multa join tipomulta on multa.codigo_multa = tipomulta.codigo_multa
  where multa.placa = pla
  group by multa.estado,tipomulta.codigo_multa,tipomulta.tipo_multa, tipomulta.monto, multa.placa;
END;
$$ LANGUAGE plpgsql;

create or replace function montoTotalMultas(cod varchar)
RETURNS INTEGER  as $$
BEGIN
  RETURN  count(multa.codigo_multa)*monto
  from multa join tipomulta on multa.codigo_multa = tipomulta.codigo_multa
  where multa.codigo_multa = cod
  group by tipomulta.monto;
END;
$$ LANGUAGE plpgsql;

create or replace procedure pago(pla varchar)
LANGUAGE plpgsql
as $$
begin
  update multa
  set estado = 'PAGADA'
  where multa.placa = pla;
end;
$$

create or replace function multasPorDepartamento(dep varchar)
RETURNS TABLE (departamento varchar, codigo_multa varchar, cantidad bigint) as $$
BEGIN
  RETURN QUERY
  select equipo.departamento, multa.codigo_multa, count(multa.codigo_multa)
  from multa join equipo on (equipo.latitud = multa.latitud and equipo.longitud = multa.longitud)
  where equipo.departamento = dep
  group by equipo.departamento, multa.codigo_multa;
END;
$$ LANGUAGE plpgsql;

create or replace function numeroMultas_RangoTiempo(f1 varchar, f2 varchar)
RETURNS TABLE (codigo_multas varchar, cantidad bigint) as $$
BEGIN
  RETURN QUERY
  SELECT codigo_multa, count(codigo_multa) from multa
  where (fecha >= f1 and fecha <= f2)
  group by codigo_multa;
END;
$$ LANGUAGE plpgsql;

create or replace function numeroMultasTiempo_departamento(f1 varchar, f2 varchar, dep varchar)
  RETURNS TABLE (departamento varchar,codigo_multas varchar, cantidad bigint) as $$
  BEGIN
    RETURN QUERY
    select equipo.departamento, multa.codigo_multa, count(multa.codigo_multa)
    from multa join equipo on (equipo.latitud = multa.latitud and equipo.longitud = multa.longitud)
    where equipo.departamento = dep and (multa.fecha >= f1 and multa.fecha <= f2)
    group by equipo.departamento, multa.codigo_multa;
  END;
  $$ LANGUAGE plpgsql;
