-- Tablas principales
CREATE TABLE Empleado (
    EmpleadoID SERIAL PRIMARY KEY,
    Nombre VARCHAR(50),
    Apellido VARCHAR(50),
    FechaNacimiento DATE,
    Email VARCHAR(100),
    Telefono VARCHAR(20),
    CargoID INT,
    UbicacionID INT,
    AreaID INT,
    TipoDocID INT
);

CREATE TABLE Cargo (
    CargoID SERIAL PRIMARY KEY,
    NombreCargo VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE Departamento (
    DeptoID SERIAL PRIMARY KEY,
    NombreDepto VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE JornadaLaboral (
    JornadaID SERIAL PRIMARY KEY,
    Tipo VARCHAR(50),
    Horas INT
);

CREATE TABLE Area (
    AreaID SERIAL PRIMARY KEY,
    NombreArea VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE Ubicacion (
    UbicacionID SERIAL PRIMARY KEY,
    Edificio VARCHAR(50),
    Piso INT,
    Oficina VARCHAR(50)
);

CREATE TABLE TipoDocumento (
    TipoDocID SERIAL PRIMARY KEY,
    NombreTipo VARCHAR(50)
);

CREATE TABLE EvaluacionDesempeno (
    EvalDesempenoID SERIAL PRIMARY KEY,
    EmpleadoID INT,
    Fecha DATE,
    Calificacion INT,
    Comentarios TEXT
);

CREATE TABLE HistorialLaboral (
    HistorialID SERIAL PRIMARY KEY,
    EmpleadoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    CargoID INT,
    DepartamentoID INT,
    Descripcion TEXT
);

CREATE TABLE Reclutamiento (
    ReclutamientoID SERIAL PRIMARY KEY,
    CargoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    Estado VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE EventoEmpleado (
    EventoID SERIAL PRIMARY KEY,
    EmpleadoID INT,
    Fecha DATE,
    TipoEvento VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE Licencias (
    LicenciaID SERIAL PRIMARY KEY,
    EmpleadoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    Motivo TEXT,
    Estado VARCHAR(50)
);

CREATE TABLE Sanciones (
    SancionID SERIAL PRIMARY KEY,
    EmpleadoID INT,
    Fecha DATE,
    TipoSancion VARCHAR(50),
    Descripcion TEXT
);

-- Tablas auxiliares
CREATE TABLE Contrato (
    ContratoID SERIAL PRIMARY KEY,
    EmpleadoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    TipoContrato VARCHAR(50),
    TipoContratoID INT
);

CREATE TABLE FormacionAcademica (
    FormacionID SERIAL PRIMARY KEY,
    EmpleadoID INT,
    Nivel VARCHAR(50),
    Institucion VARCHAR(100),
    Especialidad VARCHAR(100)
);

CREATE TABLE Salario (
    SalarioID SERIAL PRIMARY KEY,
    EmpleadoID INT,
    Monto DECIMAL(10, 2),
    FechaInicio DATE,
    FechaFin DATE,
    FechaActualizacion DATE
);

CREATE TABLE Capacitacion (
    CapacitacionID SERIAL PRIMARY KEY,
    EmpleadoID INT,
    Nombre VARCHAR(100),
    Institucion VARCHAR(100),
    FechaInicio DATE,
    FechaFin DATE
);

CREATE TABLE Beneficios (
    BeneficioID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Descripcion TEXT
);

-- Relaciones entre tablas
ALTER TABLE Empleado ADD CONSTRAINT fk_cargo FOREIGN KEY (CargoID) REFERENCES Cargo(CargoID);
ALTER TABLE Empleado ADD CONSTRAINT fk_ubicacion FOREIGN KEY (UbicacionID) REFERENCES Ubicacion(UbicacionID);
ALTER TABLE Empleado ADD CONSTRAINT fk_area FOREIGN KEY (AreaID) REFERENCES Area(AreaID);
ALTER TABLE Empleado ADD CONSTRAINT fk_tipodoc FOREIGN KEY (TipoDocID) REFERENCES TipoDocumento(TipoDocID);
ALTER TABLE EvaluacionDesempeno ADD CONSTRAINT fk_empleado FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID);
ALTER TABLE HistorialLaboral ADD CONSTRAINT fk_empleado_historial FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID);
ALTER TABLE HistorialLaboral ADD CONSTRAINT fk_cargo_historial FOREIGN KEY (CargoID) REFERENCES Cargo(CargoID);
ALTER TABLE HistorialLaboral ADD CONSTRAINT fk_departamento_historial FOREIGN KEY (DepartamentoID) REFERENCES Departamento(DeptoID);
ALTER TABLE Reclutamiento ADD CONSTRAINT fk_cargo_reclutamiento FOREIGN KEY (CargoID) REFERENCES Cargo(CargoID);
ALTER TABLE EventoEmpleado ADD CONSTRAINT fk_empleado_evento FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID);
ALTER TABLE Licencias ADD CONSTRAINT fk_empleado_licencia FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID);
ALTER TABLE Sanciones ADD CONSTRAINT fk_empleado_sancion FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID);
ALTER TABLE Contrato ADD CONSTRAINT fk_empleado_contrato FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID);
ALTER TABLE FormacionAcademica ADD CONSTRAINT fk_empleado_formacion FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID);
ALTER TABLE Salario ADD CONSTRAINT fk_empleado_salario FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID);
ALTER TABLE Capacitacion ADD CONSTRAINT fk_empleado_capacitacion FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID);


--INGRESO A LA METADATA

/*
Para acceder a la metadata en PostgreSQL, puedes utilizar consultas a las tablas del sistema que almacenan información sobre la base de datos, tablas, columnas, etc. Una forma común de acceder a la metadata es utilizando las siguientes tablas del sistema:

pg_catalog.pg_tables: Contiene información sobre las tablas en la base de datos.
pg_catalog.pg_columns: Proporciona información sobre las columnas de las tablas.
pg_catalog.pg_indexes: Contiene información sobre los índices de las tablas.
pg_catalog.pg_views: Información sobre las vistas en la base de datos.
pg_catalog.pg_constraint: Detalles sobre las restricciones de integridad en las tablas.


*/

SELECT * 
FROM pg_catalog.pg_tables 
WHERE schemaname = 'public';





-- Crear un usuario: Puedes crear un nuevo usuario con el comando  CREATE ROLE y luego asignarle una contraseña con ALTER ROLE:

CREATE ROLE nombre_usuario WITH LOGIN PASSWORD 'tu_contraseña';


--Modificar un usuario: Para modificar un usuario existente, puedes utilizar el comando ALTER ROLE:

ALTER ROLE nombre_usuario WITH PASSWORD 'nueva_contraseña';


--Eliminar un usuario: Para eliminar un usuario, puedes utilizar el comando DROP ROLE:

DROP ROLE nombre_usuario;

--Crear un Rol: Puedes crear un nuevo rol con el comando CREATE ROLE:

CREATE ROLE nombre_rol;

--Asignar un Rol a un Usuario: Puedes asignar un rol a un usuario utilizando el comando GRANT:

GRANT nombre_rol TO nombre_usuario;





--Creaciones de roles

CREATE ROLE rol_administrador;
CREATE ROLE rol_supervisor;
CREATE ROLE rol_analista;
CREATE ROLE rol_coordinador;
CREATE ROLE rol_gerente;
CREATE ROLE rol_asistente;
CREATE ROLE rol_pasante;

-- Creacion de usuarios

CREATE ROLE usuario1 WITH LOGIN PASSWORD 'contraseña1';
GRANT rol_administrador TO usuario1;


CREATE ROLE usuario2 WITH LOGIN PASSWORD 'contraseña2';
GRANT rol_supervisor TO usuario2;

CREATE ROLE usuario3 WITH LOGIN PASSWORD 'contraseña3';
GRANT rol_analista TO usuario3;

CREATE ROLE usuario4 WITH LOGIN PASSWORD 'contraseña4';
GRANT rol_coordinador TO usuario4;



-- Para ver roles en mi BD
SELECT rolname FROM pg_roles;


--Para ver lo usuarios asignados con sus ROLES

SELECT rolname, usename
FROM pg_auth_members
JOIN pg_roles ON pg_roles.oid = roleid
JOIN pg_user ON pg_user.usesysid = member;




--Conocer el nombre de usuario y nombre de la BD
SELECT current_database();
SELECT current_user;


--Para respaldar la BD de gestión de talento humano en un archivo llamado backup_gestion_talento.sql ejecutamos el siguiente comando:


pg_dump -U tu_usuario -d nombre_basedatos -f backup_gestion_talento.sql



--Para listar los atributos por entidades en tu base de datos, puedes ejecutar consultas SQL para cada tabla. 
--Aquí tienes un ejemplo de cómo listar los atributos de la tabla "Empleado":

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'Empleado';
