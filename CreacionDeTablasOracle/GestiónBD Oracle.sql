-- Tablas principales
CREATE TABLE Empleado (
EmpleadoID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
Nombre VARCHAR2(50),
Apellido VARCHAR2(50),
FechaNacimiento DATE,
Email VARCHAR2(100),
Telefono VARCHAR2(20),
CargoID NUMBER,
UbicacionID NUMBER,
AreaID NUMBER,
TipoDocID NUMBER
);

CREATE TABLE Cargo (
CargoID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
NombreCargo VARCHAR2(50),
Descripcion CLOB
);

CREATE TABLE Departamento (
DeptoID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
NombreDepto VARCHAR2(50),
Descripcion CLOB
);

CREATE TABLE JornadaLaboral (
JornadaID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
Tipo VARCHAR2(50),
Horas NUMBER
);

CREATE TABLE Area (
AreaID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
NombreArea VARCHAR2(50),
Descripcion CLOB
);

CREATE TABLE Ubicacion (
UbicacionID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
Edificio VARCHAR2(50),
Piso NUMBER,
Oficina VARCHAR2(50)
);

CREATE TABLE TipoDocumento (
TipoDocID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
NombreTipo VARCHAR2(50)
);

CREATE TABLE EvaluacionDesempeno (
EvalDesempenoID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
EmpleadoID NUMBER,
Fecha DATE,
Calificacion NUMBER,
Comentarios CLOB
);

CREATE TABLE HistorialLaboral (
HistorialID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
EmpleadoID NUMBER,
FechaInicio DATE,
FechaFin DATE,
CargoID NUMBER,
DepartamentoID NUMBER,
Descripcion CLOB
);

CREATE TABLE Reclutamiento (
ReclutamientoID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
CargoID NUMBER,
FechaInicio DATE,
FechaFin DATE,
Estado VARCHAR2(50),
Descripcion CLOB
);

CREATE TABLE EventoEmpleado (
EventoID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
EmpleadoID NUMBER,
Fecha DATE,
TipoEvento VARCHAR2(50),
Descripcion CLOB
);

CREATE TABLE Licencias (
LicenciaID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
EmpleadoID NUMBER,
FechaInicio DATE,
FechaFin DATE,
Motivo CLOB,
Estado VARCHAR2(50)
);

CREATE TABLE Sanciones (
SancionID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
EmpleadoID NUMBER,
Fecha DATE,
TipoSancion VARCHAR2(50),
Descripcion CLOB
);

-- Tablas auxiliares
CREATE TABLE Contrato (
ContratoID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
EmpleadoID NUMBER,
FechaInicio DATE,
FechaFin DATE,
TipoContrato VARCHAR2(50),
TipoContratoID NUMBER
);

CREATE TABLE FormacionAcademica (
FormacionID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
EmpleadoID NUMBER,
Nivel VARCHAR2(50),
Institucion VARCHAR2(100),
Especialidad VARCHAR2(100)
);

CREATE TABLE Salario (
SalarioID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
EmpleadoID NUMBER,
Monto NUMBER(10,2),
FechaInicio DATE,
FechaFin DATE,
FechaActualizacion DATE
);

CREATE TABLE Capacitacion (
CapacitacionID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
EmpleadoID NUMBER,
Nombre VARCHAR2(100),
Institucion VARCHAR2(100),
FechaInicio DATE,
FechaFin DATE
);

CREATE TABLE Beneficios (
BeneficioID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
Nombre VARCHAR2(100),
Descripcion CLOB
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

-- Creación de usuarios y roles
CREATE USER usuario1 IDENTIFIED BY 'contraseña1';
CREATE ROLE rola_administrador;
GRANT rola_administrador TO usuario1;

CREATE USER usuario2 IDENTIFIED BY 'contraseña2';
CREATE ROLE rol_supervisor;
GRANT rol_supervisor TO usuario2;

CREATE USER usuario3 IDENTIFIED BY 'contraseña3';
CREATE ROLE rol_analista;
GRANT rol_analista TO usuario3;

CREATE USER usuario4 IDENTIFIED BY 'contraseña4';
CREATE ROLE rol_coordinador;
GRANT rol_coordinador TO usuario4;

-- Para ver roles en mi BD
SELECT role_name FROM dba_roles;

-- Para ver los usuarios asignados con sus roles
SELECT grantee, granted_role
FROM dba_role_privs;

-- Conocer el nombre de usuario y nombre de la BD
SELECT user FROM dual;
SELECT sys_context('USERENV', 'DATABASE_NAME') FROM dual