
        CREATE TRIGGER auditoria1_AFTER_INSERT AFTER INSERT ON auditoria1
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (nombre_tabla, operacion, usuario_actual, detalle_nuevo)
            VALUES ('auditoria1', 'INSERT', USER(), CONCAT_WS(',', NEW.id, NEW.nombre_tabla, NEW.operacion, NEW.usuario_actual, NEW.fecha_hora, NEW.detalle_anterior, NEW.detalle_nuevo));
        END;
        