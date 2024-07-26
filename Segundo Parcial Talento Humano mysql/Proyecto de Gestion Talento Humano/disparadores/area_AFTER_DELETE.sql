
        CREATE TRIGGER area_AFTER_DELETE AFTER DELETE ON area
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (nombre_tabla, operacion, usuario_actual, detalle_anterior)
            VALUES ('area', 'DELETE', USER(), CONCAT_WS(',', OLD.AreaID, OLD.NombreArea, OLD.Descripcion));
        END;
        