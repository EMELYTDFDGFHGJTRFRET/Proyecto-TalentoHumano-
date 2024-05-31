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



INSERT INTO Cargo (NombreCargo, Descripcion) VALUES ('Analista de Recursos Humanos', 'Encargado de analizar y gestionar la información relacionada con el personal');
INSERT INTO Cargo (NombreCargo, Descripcion) VALUES ('Coordinador de Capacitación', 'Responsable de coordinar programas de capacitación para el desarrollo del personal');
INSERT INTO Cargo (NombreCargo, Descripcion) VALUES ('Especialista en Compensaciones', 'Encargado de diseñar y administrar los sistemas de compensación para los empleados');
INSERT INTO Cargo (NombreCargo, Descripcion) VALUES ('Asistente de Selección de Personal', 'Apoya en el proceso de reclutamiento y selección de candidatos');
INSERT INTO Cargo (NombreCargo, Descripcion) VALUES ('Gerente de Desarrollo Organizacional', 'Encargado de liderar las estrategias de desarrollo y crecimiento de la organización');

INSERT INTO Departamento (NombreDepto, Descripcion) VALUES ('Gestión del Talento Humano', 'Departamento encargado de la gestión integral del personal en la empresa');
INSERT INTO Departamento (NombreDepto, Descripcion) VALUES ('Relaciones Laborales', 'Departamento responsable de gestionar las relaciones entre la empresa y los empleados');
INSERT INTO Departamento (NombreDepto, Descripcion) VALUES ('Bienestar Laboral', 'Departamento encargado de promover el bienestar y la calidad de vida en el trabajo');
INSERT INTO Departamento (NombreDepto, Descripcion) VALUES ('Desarrollo Organizacional', 'Departamento dedicado al crecimiento y desarrollo de los colaboradores y la organización');
INSERT INTO Departamento (NombreDepto, Descripcion) VALUES ('Compensaciones y Beneficios', 'Departamento responsable de diseñar y administrar los sistemas de compensación y beneficios para los empleados');


INSERT INTO JornadaLaboral (Tipo, Horas) VALUES ('Parcial', 20);
INSERT INTO JornadaLaboral (Tipo, Horas) VALUES ('Flexible', 30);
INSERT INTO JornadaLaboral (Tipo, Horas) VALUES ('Nocturna', 35);
INSERT INTO JornadaLaboral (Tipo, Horas) VALUES ('Remota', 40);
INSERT INTO JornadaLaboral (Tipo, Horas) VALUES ('Intermitente', 25);

INSERT INTO Area (NombreArea, Descripcion) VALUES ('Desarrollo Organizacional', 'Área encargada del crecimiento y desarrollo de los colaboradores y la organización');
INSERT INTO Area (NombreArea, Descripcion) VALUES ('Gestión del Talento', 'Área dedicada a identificar, atraer y retener el talento en la empresa');
INSERT INTO Area (NombreArea, Descripcion) VALUES ('Bienestar Laboral', 'Área encargada de promover el bienestar y la calidad de vida en el trabajo');
INSERT INTO Area (NombreArea, Descripcion) VALUES ('Relaciones Laborales', 'Área responsable de gestionar las relaciones entre la empresa y los empleados');
INSERT INTO Area (NombreArea, Descripcion) VALUES ('Compensaciones y Beneficios', 'Área dedicada a diseñar y administrar los sistemas de compensación y beneficios para los empleados');

INSERT INTO Ubicacion (Edificio, Piso, Oficina) VALUES ('Torre A', 10, 'Oficina 1001');
INSERT INTO Ubicacion (Edificio, Piso, Oficina) VALUES ('Edificio Central', 5, 'Oficina 501');
INSERT INTO Ubicacion (Edificio, Piso, Oficina) VALUES ('Edificio Ejecutivo', 3, 'Oficina 303');
INSERT INTO Ubicacion (Edificio, Piso, Oficina) VALUES ('Centro Empresarial', 8, 'Oficina 801');
INSERT INTO Ubicacion (Edificio, Piso, Oficina) VALUES ('Complejo Corporativo', 12, 'Oficina 1201');


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




-- Procedimiento para insertar en Empleado
CREATE OR REPLACE FUNCTION InsertEmpleado(
    p_Nombre VARCHAR,
    p_Apellido VARCHAR,
    p_FechaNacimiento DATE,
    p_Email VARCHAR,
    p_Telefono VARCHAR,
    p_CargoID INT,
    p_UbicacionID INT,
    p_AreaID INT,
    p_TipoDocID INT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Empleado (Nombre, Apellido, FechaNacimiento, Email, Telefono, CargoID, UbicacionID, AreaID, TipoDocID)
    VALUES (p_Nombre, p_Apellido, p_FechaNacimiento, p_Email, p_Telefono, p_CargoID, p_UbicacionID, p_AreaID, p_TipoDocID);
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para seleccionar de Empleado
CREATE OR REPLACE FUNCTION SelectEmpleado() RETURNS TABLE (
    EmpleadoID INT,
    Nombre VARCHAR,
    Apellido VARCHAR,
    FechaNacimiento DATE,
    Email VARCHAR,
    Telefono VARCHAR,
    CargoID INT,
    UbicacionID INT,
    AreaID INT,
    TipoDocID INT
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM Empleado;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para actualizar en Empleado
CREATE OR REPLACE FUNCTION UpdateEmpleado(
    p_EmpleadoID INT,
    p_Nombre VARCHAR,
    p_Apellido VARCHAR,
    p_FechaNacimiento DATE,
    p_Email VARCHAR,
    p_Telefono VARCHAR,
    p_CargoID INT,
    p_UbicacionID INT,
    p_AreaID INT,
    p_TipoDocID INT
) RETURNS VOID AS $$
BEGIN
    UPDATE Empleado
    SET Nombre = p_Nombre,
        Apellido = p_Apellido,
        FechaNacimiento = p_FechaNacimiento,
        Email = p_Email,
        Telefono = p_Telefono,
        CargoID = p_CargoID,
        UbicacionID = p_UbicacionID,
        AreaID = p_AreaID,
        TipoDocID = p_TipoDocID
    WHERE EmpleadoID = p_EmpleadoID;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para eliminar en Empleado
CREATE OR REPLACE FUNCTION DeleteEmpleado(
    p_EmpleadoID INT
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Empleado WHERE EmpleadoID = p_EmpleadoID;
END;
$$ LANGUAGE plpgsql;



-- Insertar un empleado
SELECT InsertEmpleado('Juan', 'Perez', '1985-05-15', 'juan.perez@example.com', '555-1234', 1, 1, 1, 1);

-- Seleccionar todos los empleados
SELECT * FROM SelectEmpleado();

-- Actualizar un empleado
SELECT UpdateEmpleado(1, 'Juan', 'Perez', '1985-05-15', 'juan.perez@correo.com', '555-4321', 2, 2, 2, 2);

-- Seleccionar todos los empleados
SELECT * FROM SelectEmpleado();

-- Eliminar un empleado
SELECT DeleteEmpleado(1);

-- Seleccionar todos los empleados
SELECT * FROM SelectEmpleado();


-- Procedimiento para insertar en Cargo
CREATE OR REPLACE FUNCTION InsertCargo(
    p_NombreCargo VARCHAR,
    p_Descripcion TEXT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Cargo (NombreCargo, Descripcion)
    VALUES (p_NombreCargo, p_Descripcion);
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para seleccionar de Cargo
CREATE OR REPLACE FUNCTION SelectCargo() RETURNS TABLE (
    CargoID INT,
    NombreCargo VARCHAR,
    Descripcion TEXT
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM Cargo;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para actualizar en Cargo
CREATE OR REPLACE FUNCTION UpdateCargo(
    p_CargoID INT,
    p_NombreCargo VARCHAR,
    p_Descripcion TEXT
) RETURNS VOID AS $$
BEGIN
    UPDATE Cargo
    SET NombreCargo = p_NombreCargo,
        Descripcion = p_Descripcion
    WHERE CargoID = p_CargoID;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para eliminar en Cargo
CREATE OR REPLACE FUNCTION DeleteCargo(
    p_CargoID INT
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Cargo WHERE CargoID = p_CargoID;
END;
$$ LANGUAGE plpgsql;



-- Insertar un cargo
SELECT InsertCargo('Gerente', 'Responsable de la gestión del departamento');

-- Seleccionar todos los cargos
SELECT * FROM SelectCargo();

-- Actualizar un cargo
SELECT UpdateCargo(1, 'Gerente General', 'Responsable de la gestión general del departamento');

-- Seleccionar todos los cargos
SELECT * FROM SelectCargo();

-- Eliminar un cargo
SELECT DeleteCargo(1);

-- Seleccionar todos los cargos
SELECT * FROM SelectCargo();



-- Función para crear un usuario
CREATE OR REPLACE FUNCTION crear_usuario(nombre_usuario VARCHAR, contraseña VARCHAR)
RETURNS VOID AS $$
BEGIN
    EXECUTE format('CREATE USER %I WITH PASSWORD %L', nombre_usuario, contraseña);
    EXECUTE format('GRANT CONNECT ON DATABASE TalentoHumano2 TO %I', nombre_usuario);
END;
$$ LANGUAGE plpgsql;

-- Función para modificar un usuario
CREATE OR REPLACE FUNCTION modificar_usuario(nombre_usuario_actual VARCHAR, nuevo_nombre_usuario VARCHAR)
RETURNS VOID AS $$
BEGIN
    EXECUTE format('ALTER USER %I RENAME TO %I', nombre_usuario_actual, nuevo_nombre_usuario);
END;
$$ LANGUAGE plpgsql;

-- Función para eliminar un usuario
CREATE OR REPLACE FUNCTION eliminar_usuario(nombre_usuario VARCHAR)
RETURNS VOID AS $$
BEGIN
    EXECUTE format('DROP USER %I CASCADE', nombre_usuario);
END;
$$ LANGUAGE plpgsql;

