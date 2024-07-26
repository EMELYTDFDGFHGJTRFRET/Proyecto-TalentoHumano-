
        CREATE TRIGGER empleado_AFTER_UPDATE AFTER UPDATE ON empleado
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (nombre_tabla, operacion, usuario_actual, detalle_anterior, detalle_nuevo)
            VALUES ('empleado', 'UPDATE', USER(), CONCAT_WS(',', OLD.EmpleadoID, OLD.Nombre, OLD.Apellido, OLD.FechaNacimiento, OLD.Email, OLD.Telefono, OLD.CargoID, OLD.UbicacionID, OLD.AreaID, OLD.TipoDocID), CONCAT_WS(',', NEW.EmpleadoID, NEW.Nombre, NEW.Apellido, NEW.FechaNacimiento, NEW.Email, NEW.Telefono, NEW.CargoID, NEW.UbicacionID, NEW.AreaID, NEW.TipoDocID));
        END;
        