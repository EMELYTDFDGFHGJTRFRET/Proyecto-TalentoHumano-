CREATE DATABASE `talento_humano` 
USE talento_humano;

-- Tablas principales
CREATE TABLE Empleado (
    EmpleadoID INT AUTO_INCREMENT PRIMARY KEY,
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
    CargoID INT AUTO_INCREMENT PRIMARY KEY,
    NombreCargo VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE Departamento (
    DeptoID INT AUTO_INCREMENT PRIMARY KEY,
    NombreDepto VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE JornadaLaboral (
    JornadaID INT AUTO_INCREMENT PRIMARY KEY,
    Tipo VARCHAR(50),
    Horas INT
);

CREATE TABLE Area (
    AreaID INT AUTO_INCREMENT PRIMARY KEY,
    NombreArea VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE Ubicacion (
    UbicacionID INT AUTO_INCREMENT PRIMARY KEY,
    Edificio VARCHAR(50),
    Piso INT,
    Oficina VARCHAR(50)
);

CREATE TABLE TipoDocumento (
    TipoDocID INT AUTO_INCREMENT PRIMARY KEY,
    NombreTipo VARCHAR(50)
);

CREATE TABLE EvaluacionDesempeno (
    EvalDesempenoID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    Fecha DATE,
    Calificacion INT,
    Comentarios TEXT,
    FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID)
);

CREATE TABLE HistorialLaboral (
    HistorialID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    CargoID INT,
    DepartamentoID INT,
    Descripcion TEXT,
    FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID),
    FOREIGN KEY (CargoID) REFERENCES Cargo(CargoID),
    FOREIGN KEY (DepartamentoID) REFERENCES Departamento(DeptoID)
);

CREATE TABLE Reclutamiento (
    ReclutamientoID INT AUTO_INCREMENT PRIMARY KEY,
    CargoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    Estado VARCHAR(50),
    Descripcion TEXT,
    FOREIGN KEY (CargoID) REFERENCES Cargo(CargoID)
);

CREATE TABLE EventoEmpleado (
    EventoID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    Fecha DATE,
    TipoEvento VARCHAR(50),
    Descripcion TEXT,
    FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID)
);

CREATE TABLE Licencias (
    LicenciaID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    Motivo TEXT,
    Estado VARCHAR(50),
    FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID)
);

CREATE TABLE Sanciones (
    SancionID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    Fecha DATE,
    TipoSancion VARCHAR(50),
    Descripcion TEXT,
    FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID)
);

-- Tablas auxiliares
CREATE TABLE Contrato (
    ContratoID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    TipoContrato VARCHAR(50),
    TipoContratoID INT,
    FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID)
);

CREATE TABLE FormacionAcademica (
    FormacionID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    Nivel VARCHAR(50),
    Institucion VARCHAR(100),
    Especialidad VARCHAR(100),
    FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID)
);

CREATE TABLE Salario (
    SalarioID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    Monto DECIMAL(10, 2),
    FechaInicio DATE,
    FechaFin DATE,
    FechaActualizacion DATE,
    FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID)
);

CREATE TABLE Capacitacion (
    CapacitacionID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    Nombre VARCHAR(100),
    Institucion VARCHAR(100),
    FechaInicio DATE,
    FechaFin DATE,
    FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID)
);

CREATE TABLE Beneficios (
    BeneficioID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100),
    Descripcion TEXT
);

-- Relaciones entre tablas
ALTER TABLE Empleado ADD CONSTRAINT fk_cargo FOREIGN KEY (CargoID) REFERENCES Cargo(CargoID);
ALTER TABLE Empleado ADD CONSTRAINT fk_ubicacion FOREIGN KEY (UbicacionID) REFERENCES Ubicacion(UbicacionID);
ALTER TABLE Empleado ADD CONSTRAINT fk_area FOREIGN KEY (AreaID) REFERENCES Area(AreaID);
ALTER TABLE Empleado ADD CONSTRAINT fk_tipodoc FOREIGN KEY (TipoDocID) REFERENCES TipoDocumento(TipoDocID);

-- Creación de usuarios y roles
CREATE USER 'nombre_usuario'@'localhost' IDENTIFIED BY 'tu_contraseña';

-- Modificar un usuario
SET PASSWORD FOR 'nombre_usuario'@'localhost' = 'nueva_contraseña';

-- Eliminar un usuario
DROP USER 'nombre_usuario'@'localhost';

-- Crear un rol
CREATE ROLE 'nombre_rol';

-- Asignar un rol a un usuario
GRANT 'nombre_rol' TO 'nombre_usuario'@'localhost';

-- Creaciones de roles
CREATE ROLE 'rol_administrador';
CREATE ROLE 'rol_supervisor';
CREATE ROLE 'rol_analista';
CREATE ROLE 'rol_coordinador';
CREATE ROLE 'rol_gerente';
CREATE ROLE 'rol_asistente';
CREATE ROLE 'rol_pasante';

-- Creación de usuarios con roles
CREATE USER 'usuario1'@'localhost' IDENTIFIED BY 'contraseña1';
GRANT 'rol_administrador' TO 'usuario1'@'localhost';

CREATE USER 'usuario2'@'localhost' IDENTIFIED BY 'contraseña2';
GRANT 'rol_supervisor' TO 'usuario2'@'localhost';

CREATE USER 'usuario3'@'localhost' IDENTIFIED BY 'contraseña3';
GRANT 'rol_analista' TO 'usuario3'@'localhost';

CREATE USER 'usuario4'@'localhost' IDENTIFIED BY 'contraseña4';
GRANT 'rol_coordinador' TO 'usuario4'@'localhost';

-- Para ver roles en la base de datos
SELECT User, Host FROM mysql.user;

-- Para ver los usuarios asignados con sus roles
SELECT * FROM mysql.user;

-- Conocer el nombre de usuario y nombre de la base de datos
SELECT DATABASE();
SELECT CURRENT_USER();

-- Para respaldar la base de datos
-- Ejecutar en línea de comandos
-- mysqldump -u tu_usuario -p nombre_basedatos > backup_gestion_talento.sql

-- Listar los atributos por entidades
SELECT COLUMN_NAME, DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'Empleado';


