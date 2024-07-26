
        CREATE TRIGGER area_AFTER_INSERT AFTER INSERT ON area
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (nombre_tabla, operacion, usuario_actual, detalle_nuevo)
            VALUES ('area', 'INSERT', USER(), CONCAT_WS(',', NEW.AreaID, NEW.NombreArea, NEW.Descripcion));
        END;
        