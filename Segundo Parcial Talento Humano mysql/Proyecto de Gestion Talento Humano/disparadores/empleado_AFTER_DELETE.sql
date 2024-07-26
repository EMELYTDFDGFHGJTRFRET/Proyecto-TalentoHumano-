
        CREATE TRIGGER empleado_AFTER_DELETE AFTER DELETE ON empleado
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (nombre_tabla, operacion, usuario_actual, detalle_anterior)
            VALUES ('empleado', 'DELETE', USER(), CONCAT_WS(',', OLD.EmpleadoID, OLD.Nombre, OLD.Apellido, OLD.FechaNacimiento, OLD.Email, OLD.Telefono, OLD.CargoID, OLD.UbicacionID, OLD.AreaID, OLD.TipoDocID));
        END;
        