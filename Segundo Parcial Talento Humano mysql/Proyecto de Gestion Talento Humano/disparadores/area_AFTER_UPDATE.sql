
        CREATE TRIGGER area_AFTER_UPDATE AFTER UPDATE ON area
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (nombre_tabla, operacion, usuario_actual, detalle_anterior, detalle_nuevo)
            VALUES ('area', 'UPDATE', USER(), CONCAT_WS(',', OLD.AreaID, OLD.NombreArea, OLD.Descripcion), CONCAT_WS(',', NEW.AreaID, NEW.NombreArea, NEW.Descripcion));
        END;
        