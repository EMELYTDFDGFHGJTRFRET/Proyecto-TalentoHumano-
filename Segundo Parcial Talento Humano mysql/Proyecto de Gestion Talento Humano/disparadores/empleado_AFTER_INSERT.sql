
        CREATE TRIGGER empleado_AFTER_INSERT AFTER INSERT ON empleado
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (nombre_tabla, operacion, usuario_actual, detalle_nuevo)
            VALUES ('empleado', 'INSERT', USER(), CONCAT_WS(',', NEW.EmpleadoID, NEW.Nombre, NEW.Apellido, NEW.FechaNacimiento, NEW.Email, NEW.Telefono, NEW.CargoID, NEW.UbicacionID, NEW.AreaID, NEW.TipoDocID));
        END;
        