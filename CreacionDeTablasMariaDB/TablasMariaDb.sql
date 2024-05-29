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
    Comentarios TEXT
);

CREATE TABLE HistorialLaboral (
    HistorialID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    CargoID INT,
    DepartamentoID INT,
    Descripcion TEXT
);

CREATE TABLE Reclutamiento (
    ReclutamientoID INT AUTO_INCREMENT PRIMARY KEY,
    CargoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    Estado VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE EventoEmpleado (
    EventoID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    Fecha DATE,
    TipoEvento VARCHAR(50),
    Descripcion TEXT
);

CREATE TABLE Licencias (
    LicenciaID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    Motivo TEXT,
    Estado VARCHAR(50)
);

CREATE TABLE Sanciones (
    SancionID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    Fecha DATE,
    TipoSancion VARCHAR(50),
    Descripcion TEXT
);

-- Tablas auxiliares
CREATE TABLE Contrato (
    ContratoID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    FechaInicio DATE,
    FechaFin DATE,
    TipoContrato VARCHAR(50),
    TipoContratoID INT
);

CREATE TABLE FormacionAcademica (
    FormacionID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    Nivel VARCHAR(50),
    Institucion VARCHAR(100),
    Especialidad VARCHAR(100)
);

CREATE TABLE Salario (
    SalarioID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    Monto DECIMAL(10, 2),
    FechaInicio DATE,
    FechaFin DATE,
    FechaActualizacion DATE
);



CREATE TABLE Capacitacion (
    CapacitacionID INT AUTO_INCREMENT PRIMARY KEY,
    EmpleadoID INT,
    Nombre VARCHAR(100),
    Institucion VARCHAR(100),
    FechaInicio DATE,
    FechaFin DATE
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


-- Consulta de tablas en MariaDB
SELECT * 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Crear un usuario en MariaDB
CREATE USER 'nombre_usuario'@'localhost' IDENTIFIED BY 'tu_contraseña';

-- Modificar la contraseña de un usuario en MariaDB
SET PASSWORD FOR 'nombre_usuario'@'localhost' = PASSWORD('nueva_contraseña');

-- Eliminar un usuario en MariaDB
DROP USER 'nombre_usuario'@'localhost';

-- Crear un rol en MariaDB
CREATE ROLE nombre_rol;

-- Asignar un rol a un usuario en MariaDB
GRANT nombre_rol TO 'nombre_usuario'@'localhost';

-- Creaciones de roles en MariaDB
CREATE ROLE rol_administrador;
CREATE ROLE rol_supervisor;
CREATE ROLE rol_analista;
CREATE ROLE rol_coordinador;
CREATE ROLE rol_gerente;
CREATE ROLE rol_asistente;
CREATE ROLE rol_pasante;

-- Creacion de usuarios en MariaDB
CREATE USER 'usuario1'@'localhost' IDENTIFIED BY 'contraseña1';
GRANT rol_administrador TO 'usuario1'@'localhost';

CREATE USER 'usuario2'@'localhost' IDENTIFIED BY 'contraseña2';
GRANT rol_supervisor TO 'usuario2'@'localhost';

CREATE USER 'usuario3'@'localhost' IDENTIFIED BY 'contraseña3';
GRANT rol_analista TO 'usuario3'@'localhost';

CREATE USER 'usuario4'@'localhost' IDENTIFIED BY 'contraseña4';
GRANT rol_coordinador TO 'usuario4'@'localhost';

-- Ver roles en MariaDB
SELECT user FROM mysql.user WHERE user = 'nombre_rol';

-- Ver usuarios asignados con sus roles en MariaDB
SELECT user, role FROM mysql.user WHERE user = 'nombre_usuario';

-- Conocer el nombre de usuario y nombre de la BD en MariaDB
SELECT DATABASE();
SELECT CURRENT_USER();

-- Para respaldar la BD en MariaDB
mysqldump -u tu_usuario -p nombre_basedatos > backup_gestion_talento.sql;

-- Listar los atributos por entidades en MariaDB
DESCRIBE Empleado;




