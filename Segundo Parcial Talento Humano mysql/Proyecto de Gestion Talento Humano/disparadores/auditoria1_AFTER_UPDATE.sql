
        CREATE TRIGGER auditoria1_AFTER_UPDATE AFTER UPDATE ON auditoria1
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (nombre_tabla, operacion, usuario_actual, detalle_anterior, detalle_nuevo)
            VALUES ('auditoria1', 'UPDATE', USER(), CONCAT_WS(',', OLD.id, OLD.nombre_tabla, OLD.operacion, OLD.usuario_actual, OLD.fecha_hora, OLD.detalle_anterior, OLD.detalle_nuevo), CONCAT_WS(',', NEW.id, NEW.nombre_tabla, NEW.operacion, NEW.usuario_actual, NEW.fecha_hora, NEW.detalle_anterior, NEW.detalle_nuevo));
        END;
        