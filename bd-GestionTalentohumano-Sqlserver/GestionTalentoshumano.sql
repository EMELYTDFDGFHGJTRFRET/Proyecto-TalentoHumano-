--GESTION DE TALENTOS HUMANOS--
-- Tablas principales
CREATE TABLE Empleado (
    EmpleadoID INT PRIMARY KEY IDENTITY,
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
    CargoID INT PRIMARY KEY IDENTITY,
    NombreCargo VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE Departamento (
    DeptoID INT PRIMARY KEY IDENTITY,
    NombreDepto VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE JornadaLaboral (
    JornadaID INT PRIMARY KEY IDENTITY,
    Tipo VARCHAR(50),
    Horas INT
);

CREATE TABLE Area (
    AreaID INT PRIMARY KEY IDENTITY,
    NombreArea VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE Ubicacion (
    UbicacionID INT PRIMARY KEY IDENTITY,
    Edificio VARCHAR(50),
    Piso INT,
    Oficina VARCHAR(50)
);

CREATE TABLE TipoDocumento (
    TipoDocID INT PRIMARY KEY IDENTITY,
    NombreTipo VARCHAR(50)
);

CREATE TABLE EvaluacionDesempeno (
    EvalDesempenoID INT PRIMARY KEY IDENTITY,
    EmpleadoID INT,
    Fecha DATE,
    Calificacion INT,
    Comentarios TEXT
);

CREATE TABLE HistorialLaboral (
    HistorialID INT PRIMARY KEY IDENTITY,
    EmpleadoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    CargoID INT,
    DepartamentoID INT,
    Descripcion TEXT
);

CREATE TABLE Reclutamiento (
    ReclutamientoID INT PRIMARY KEY IDENTITY,
    CargoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    Estado VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE EventoEmpleado (
    EventoID INT PRIMARY KEY IDENTITY,
    EmpleadoID INT,
    Fecha DATE,
    TipoEvento VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE Licencias (
    LicenciaID INT PRIMARY KEY IDENTITY,
    EmpleadoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    Motivo TEXT,
    Estado VARCHAR(50)
);

CREATE TABLE Sanciones (
    SancionID INT PRIMARY KEY IDENTITY,
    EmpleadoID INT,
    Fecha DATE,
    TipoSancion VARCHAR(50),
    Descripcion TEXT
);

-- Tablas auxiliares
CREATE TABLE Contrato (
    ContratoID INT PRIMARY KEY IDENTITY,
    EmpleadoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    TipoContrato VARCHAR(50),
    TipoContratoID INT
);

CREATE TABLE FormacionAcademica (
    FormacionID INT PRIMARY KEY IDENTITY,
    EmpleadoID INT,
    Nivel VARCHAR(50),
    Institucion VARCHAR(100),
    Especialidad VARCHAR(100)
);

CREATE TABLE Salario (
    SalarioID INT PRIMARY KEY IDENTITY,
    EmpleadoID INT,
    Monto DECIMAL(10, 2),
    FechaInicio DATE,
    FechaFin DATE,
    FechaActualizacion DATE
);

CREATE TABLE Capacitacion (
    CapacitacionID INT PRIMARY KEY IDENTITY,
    EmpleadoID INT,
    Nombre VARCHAR(100),
    Institucion VARCHAR(100),
    FechaInicio DATE,
    FechaFin DATE
);

CREATE TABLE Beneficios (
    BeneficioID INT PRIMARY KEY IDENTITY,
    Nombre VARCHAR(100),
    Descripcion TEXT
);

--RELACIONES ENTRE TODAS LAS TABLAS
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
Para acceder a la metadata en sqlServer, puedes utilizar consultas a las tablas del sistema que almacenan información sobre la base de datos, tablas, columnas, etc. Una forma común de acceder a la metadata es utilizando las siguientes tablas del sistema:
SELECT * FROM INFORMATION_SCHEMA.TABLES; Contiene información sobre las tablas en la base de datos.
SELECT * FROM INFORMATION_SCHEMA.COLUMNS; Proporciona información sobre las columnas de las tablas.

SELECT 
    t.name AS TableName,
    i.name AS IndexName,
    c.name AS ColumnName

FROM 
    sys.indexes i
    INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
    INNER JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
    INNER JOIN sys.tables t ON i.object_id = t.object_id

WHERE 
    i.is_primary_key = 0; -- Exclude primary key indexes    --Contiene información sobre los índices de las tablas.--
SELECT * FROM INFORMATION_SCHEMA.VIEWS; Información sobre las vistas en la base de datos.

--Detalles sobre las restricciones de integridad en las tablas.--
-- Información general sobre las restricciones en las tablas
SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS;
-- Información sobre restricciones referenciales (foreign keys)
SELECT * FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS;
-- Información sobre columnas usadas en restricciones
SELECT * FROM INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE;
*/

SELECT * 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'dbo';


-- CREAR UN USUARIO:--
-- Crear el inicio de sesión (login) en el servidor
CREATE LOGIN nombre_usuario WITH PASSWORD = 'tu_contraseña';
-- Cambiar al contexto de la base de datos
USE NombreBaseDatos;
-- Crear el usuario en la base de datos y asignarlo al inicio de sesión
CREATE USER nombre_usuario FOR LOGIN nombre_usuario;


--Modificar un usuario: Para modificar cambiar contraseña a un usuario existente, puedes utilizar el comando:--
ALTER LOGIN nombre_usuario WITH PASSWORD = 'nueva_contraseña';

--Eliminar un usuario: Para eliminar un usuario, puedes utilizar el comando:--
DROP USER nombre_usuario;

--Crear un Rol: Puedes crear un nuevo rol con el comando:--
CREATE ROLE nombre_rol;

--Asignar un Rol a un Usuario: Puedes asignar un rol a un usuario utilizando el comando:--
ALTER ROLE nombre_rol ADD MEMBER nombre_usuario;


--Creaciones de roles--
CREATE ROLE rol_administrador;
CREATE ROLE rol_supervisor;
CREATE ROLE rol_analista;
CREATE ROLE rol_coordinador;
CREATE ROLE rol_gerente;
CREATE ROLE rol_asistente;
CREATE ROLE rol_pasante;


--Creaciones de usuarios--
-- Crear un login y asignarle un rol
CREATE LOGIN usuario1 WITH PASSWORD = 'contraseña1';
CREATE USER usuario1 FOR LOGIN usuario1;
ALTER ROLE rol_administrador ADD MEMBER usuario1;

-- Repite estos pasos para otros usuarios y roles
CREATE LOGIN usuario2 WITH PASSWORD = 'contraseña2';
CREATE USER usuario2 FOR LOGIN usuario2;
ALTER ROLE rol_supervisor ADD MEMBER usuario2;

CREATE LOGIN usuario3 WITH PASSWORD = 'contraseña3';
CREATE USER usuario3 FOR LOGIN usuario3;
ALTER ROLE rol_analista ADD MEMBER usuario3;

CREATE LOGIN usuario4 WITH PASSWORD = 'contraseña4';
CREATE USER usuario4 FOR LOGIN usuario4;
ALTER ROLE rol_coordinador ADD MEMBER usuario4;


-- Para ver roles en mi BD
SELECT name 
FROM sys.database_principals 
WHERE type_desc = 'DATABASE_ROLE';


--Para ver lo usuarios asignados con sus ROLES
SELECT r.name AS rolname, u.name AS username
FROM sys.database_role_members rm
JOIN sys.database_principals r ON rm.role_principal_id = r.principal_id
JOIN sys.database_principals u ON rm.member_principal_id = u.principal_id
WHERE r.type_desc = 'DATABASE_ROLE' AND u.type_desc = 'SQL_USER';

--Conocer el nombre de usuario y nombre de la BD
SELECT DB_NAME() AS NombreBaseDatos;
SELECT CURRENT_USER AS NombreUsuario;


--Para respaldar la BD de gestión de talento humano en un archivo llamado backup_gestion_talento.sql ejecutamos el siguiente comando:
BACKUP DATABASE nombre_basedatos TO DISK = 'Ruta\backup_gestion_talento.bak';


--Para listar los atributos por entidades en tu base de datos, puedes ejecutar consultas sqlserver para cada tabla. 
--Aquí tienes un ejemplo de cómo listar los atributos de la tabla "Empleado":
SELECT c.name AS column_name, t.name AS data_type
FROM sys.columns c
INNER JOIN sys.types t ON c.user_type_id = t.user_type_id
WHERE OBJECT_NAME(c.object_id) = 'Empleado';
