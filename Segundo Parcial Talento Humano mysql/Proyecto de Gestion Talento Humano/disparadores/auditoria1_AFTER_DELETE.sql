
        CREATE TRIGGER auditoria1_AFTER_DELETE AFTER DELETE ON auditoria1
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (nombre_tabla, operacion, usuario_actual, detalle_anterior)
            VALUES ('auditoria1', 'DELETE', USER(), CONCAT_WS(',', OLD.id, OLD.nombre_tabla, OLD.operacion, OLD.usuario_actual, OLD.fecha_hora, OLD.detalle_anterior, OLD.detalle_nuevo));
        END;
        