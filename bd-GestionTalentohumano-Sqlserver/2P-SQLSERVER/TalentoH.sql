
--PRUEBA1
INSERT INTO [dbo].[prueba1] (Nombre_tabla, operacion, usuario_actual, detalle_anterior, detalle_nuevo)
VALUES ('Pedro', 'insert', 'usuario', 'Desarrollador','nuevo insert');
INSERT INTO [dbo].[prueba1] (Nombre_tabla, operacion, usuario_actual, detalle_anterior, detalle_nuevo)
VALUES ('Ana', 'insert', 'usuario', 'Desarrollador','nuevo insert');
INSERT INTO [dbo].[prueba1] (Nombre_tabla, operacion, usuario_actual, detalle_anterior, detalle_nuevo)
VALUES ('Ivania', 'insert', 'usuario', 'Desarrollador','nuevo insert');

UPDATE [dbo].[prueba1]  --Modificar--
SET Nombre_tabla = 'trabajo',
    operacion = 'update',
    usuario_actual = 'usuario_modificador',
    detalle_anterior = 'Desarrollador',
    detalle_nuevo = 'Senior Desarrollador'
WHERE ID = 3;


DELETE FROM [dbo].[prueba1] --Eliminar ID--
WHERE ID = 2;




--PRUEBA2
INSERT INTO [dbo].[prueba2] (Nombre_tabla, operacion, usuario_actual, detalle_anterior, detalle_nuevo)
VALUES ('Pablo', 'insert', 'usuario', 'Desarrollador','nuevo insert');
INSERT INTO [dbo].[prueba2] (Nombre_tabla, operacion, usuario_actual, detalle_anterior, detalle_nuevo)
VALUES ('Dayana', 'insert', 'usuario', 'Desarrollador','nuevo insert');
INSERT INTO [dbo].[prueba2] (Nombre_tabla, operacion, usuario_actual, detalle_anterior, detalle_nuevo)
VALUES ('Evelyn', 'insert', 'usuario', 'Desarrollador','nuevo insert');


UPDATE [dbo].[prueba2]
SET Nombre_tabla = 'empleado',
    operacion = 'update',
    usuario_actual = 'usuario_modificador',
    detalle_anterior = 'Desarrollador',
    detalle_nuevo = 'Senior Desarrollador'
WHERE ID = 2;


DELETE FROM [dbo].[prueba2]
WHERE ID = 3;


SELECT * FROM [dbo].[prueba1];
SELECT * FROM [dbo].[prueba2];
SELECT * FROM [dbo].[auditoria];