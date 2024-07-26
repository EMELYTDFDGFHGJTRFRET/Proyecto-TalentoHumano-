import mysql.connector
from mysql.connector import errorcode
from fpdf import FPDF
import os
from datetime import datetime

config = {
    'user': 'root',
    'password': '123456',
    'host': 'localhost',
    'database': 'GestionTalentoHumano',
}

def main():
    while True:
        print("\nSeleccione una opción:")
        print("1. Crear Usuario")
        print("2. Modificar Usuario")
        print("3. Eliminar Usuario")
        print("4. Crear Rol")
        print("5. Asignar Rol a Usuario")
        print("6. Consultar Roles")
        print("7. Consultar Usuarios")
        print("8. Realizar respaldo de la base de datos")
        print("9. Restaurar base de datos")
        print("10. Listar las entidades")
        print("11. Listar atributos por entidades")
        print("12. Agregar entidades con atributos")
        print("13. Generar reporte en PDF")
        print("14. Salir")
        print("15. Procedimientos almacenados")
        print("---------SegundoPacrial---------------")
        print("16. Ver todas las tablas y sus atributos")
        print("17. Crear Tabla de Auditoría")
        print("18. Generar Triggers de cada entidad")
        print("19. Gestionar logs de eventos y auditoría")
        print("20. Generar informe PDF de tabla o descargar triggers")
        opcion = input("Ingrese la opción seleccionada: ")

        if not opcion.isdigit() or int(opcion) not in range(1, 21):
            print("Opción no válida. Por favor, ingrese un número del 1 al 20.")
            continue

        opcion = int(opcion)
        if opcion == 1:
            crear_login_y_usuario()
        elif opcion == 2:
            modificar_usuario()
        elif opcion == 3:
            eliminar_usuario()
        elif opcion == 4:
            crear_rol()
        elif opcion == 5:
            asignar_rol_usuario()
        elif opcion == 6:
            consultar_roles()
        elif opcion == 7:
            consultar_usuarios()
        elif opcion == 8:
            realizar_respaldo()
        elif opcion == 9:
            restaurar_base_de_datos()
        elif opcion == 10:
            listar_entidades_base_datos()
        elif opcion == 11:
            listar_atributos_entidad()
        elif opcion == 12:
            agregar_entidad_con_atributos()
        elif opcion == 13:
            generar_informe_pdf()
        elif opcion == 14:
            break
        elif opcion == 15:
            generar_procedimientos_almacenados()
        elif opcion == 16:
            ver_tablas_y_atributos()
        elif opcion == 17:
            crear_tabla_auditoria()
        elif opcion == 18:
            nombre_tabla = input("Ingrese el nombre de la tabla para generar los triggers de auditoría: ")
            generar_triggers_auditoria(nombre_tabla)
        elif opcion == 19:
            gestionar_logs_eventos_auditoria()
        elif opcion == 20:
            generar_informe_o_descargar_triggers()
        else:
            print("Opción no válida. Por favor, ingrese un número del 1 al 20.")

def crear_login_y_usuario():
    nombre_login = input("Ingrese el nombre del nuevo login: ")
    contraseña_login = input("Ingrese la contraseña del nuevo login: ")

    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        verificar_login_query = "SELECT user FROM mysql.user WHERE user = %s"
        cursor.execute(verificar_login_query, (nombre_login,))
        resultado = cursor.fetchone()
        if resultado:
            print(f"El login '{nombre_login}' ya existe en el servidor.")
            return

        create_login_query = f"CREATE USER '{nombre_login}'@'localhost' IDENTIFIED BY '{contraseña_login}'"
        cursor.execute(create_login_query)
        print(f"Login '{nombre_login}' creado correctamente.")

        nombre_base_de_datos = input("Ingrese el nombre de la base de datos para crear el usuario: ")
        verificar_base_de_datos_query = "SHOW DATABASES LIKE %s"
        cursor.execute(verificar_base_de_datos_query, (nombre_base_de_datos,))
        resultado = cursor.fetchone()
        if not resultado:
            print(f"La base de datos '{nombre_base_de_datos}' no existe en el servidor.")
            return

        grant_privileges_query = f"GRANT ALL PRIVILEGES ON {nombre_base_de_datos}.* TO '{nombre_login}'@'localhost'"
        cursor.execute(grant_privileges_query)
        print(f"Usuario '{nombre_login}' creado correctamente en la base de datos '{nombre_base_de_datos}'.")
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def modificar_usuario():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        obtener_usuarios_query = "SELECT User FROM mysql.user"
        cursor.execute(obtener_usuarios_query)
        usuarios = cursor.fetchall()

        for i, usuario in enumerate(usuarios, 1):
            print(f"{i}. {usuario[0]}")

        seleccion = int(input("Ingrese el número del usuario a modificar: "))
        nombre_usuario = usuarios[seleccion - 1][0]
        nuevo_nombre_usuario = input("Ingrese el nuevo nombre para el usuario: ")

        query = f"RENAME USER '{nombre_usuario}'@'localhost' TO '{nuevo_nombre_usuario}'@'localhost'"
        cursor.execute(query)
        connection.commit()
        print(f"Usuario '{nombre_usuario}' modificado correctamente. Nuevo nombre: '{nuevo_nombre_usuario}'")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def eliminar_usuario():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        obtener_usuarios_query = "SELECT User FROM mysql.user"
        cursor.execute(obtener_usuarios_query)
        usuarios = cursor.fetchall()

        for i, usuario in enumerate(usuarios, 1):
            print(f"{i}. {usuario[0]}")

        seleccion = int(input("Ingrese el número del usuario a eliminar: "))
        nombre_usuario = usuarios[seleccion - 1][0]

        eliminar_usuario_query = f"DROP USER '{nombre_usuario}'@'localhost'"
        cursor.execute(eliminar_usuario_query)
        connection.commit()
        print(f"Usuario '{nombre_usuario}' eliminado correctamente.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def crear_rol():
    nombre_rol = input("Ingrese el nombre del nuevo rol: ")
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = f"CREATE ROLE '{nombre_rol}'"
        cursor.execute(query)
        connection.commit()
        print(f"Rol '{nombre_rol}' creado correctamente.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def asignar_rol_usuario():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        obtener_usuarios_query = "SELECT User FROM mysql.user"
        cursor.execute(obtener_usuarios_query)
        usuarios = cursor.fetchall()

        print("Usuarios disponibles:")
        for i, usuario in enumerate(usuarios, 1):
            print(f"{i}. {usuario[0]}")

        seleccion_usuario = int(input("Ingrese el número del usuario: "))
        nombre_usuario = usuarios[seleccion_usuario - 1][0]

        obtener_roles_query = "SELECT User FROM mysql.user WHERE host = 'localhost' AND user = %s"
        cursor.execute(obtener_roles_query, (nombre_usuario,))
        roles = cursor.fetchall()

        print("Roles disponibles:")
        for i, rol in enumerate(roles, 1):
            print(f"{i}. {rol[0]}")

        seleccion_rol = int(input("Ingrese el número del rol: "))
        nombre_rol = roles[seleccion_rol - 1][0]

        query = f"GRANT '{nombre_rol}' TO '{nombre_usuario}'@'localhost'"
        cursor.execute(query)
        connection.commit()
        print(f"Rol '{nombre_rol}' asignado al usuario '{nombre_usuario}' correctamente.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def consultar_roles():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SELECT User FROM mysql.user WHERE host = 'localhost'")
        for (name,) in cursor:
            print(name)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def consultar_usuarios():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SELECT User FROM mysql.user")
        for (username,) in cursor:
            print(username)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def realizar_respaldo():
    try:
        database_name = input("Ingrese el nombre de la base de datos a respaldar: ")
        file_name = input("Ingrese el nombre del archivo de respaldo (.sql): ")
        backup_folder_path = "/path/to/backup/folder"
        backup_file_name = os.path.join(backup_folder_path, file_name)

        if os.path.exists(backup_file_name):
            print("El archivo de respaldo ya existe en la ubicación especificada.")
            return

        os.system(f"mysqldump -u {config['user']} -p{config['password']} {database_name} > {backup_file_name}")
        print(f"Respaldo de la base de datos '{database_name}' creado correctamente en '{backup_file_name}'.")
    except Exception as ex:
        print(f"Error al realizar el respaldo: {ex}")

def restaurar_base_de_datos():
    try:
        backup_path = "/path/to/backup/folder"
        backup_files = [f for f in os.listdir(backup_path) if f.endswith(".sql")]

        if backup_files:
            print("Seleccione el archivo de respaldo a restaurar:")
            for i, file in enumerate(backup_files, 1):
                print(f"{i}. {file}")

            selected_index = int(input("Ingrese el número correspondiente: ")) - 1
            backup_file_path = os.path.join(backup_path, backup_files[selected_index])
            database_name = input("Ingrese el nombre de la base de datos a restaurar: ")

            os.system(f"mysql -u {config['user']} -p{config['password']} {database_name} < {backup_file_path}")
            print(f"Se restauró la base de datos '{database_name}' desde el archivo '{backup_files[selected_index]}'.")
        else:
            print("No hay archivos de respaldo disponibles.")
    except Exception as ex:
        print(f"Error al restaurar la base de datos: {ex}")

def listar_entidades_base_datos():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        print("Lista de entidades en la base de datos:")
        for (table_name,) in cursor:
            print(f"- {table_name}")
    except mysql.connector.Error as err:
        print(f"Error al listar las entidades: {err}")
    finally:
        cursor.close()
        connection.close()

def listar_atributos_entidad():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print("Lista de entidades en la base de datos:")
        for i, (table_name,) in enumerate(tables, 1):
            print(f"{i}. {table_name}")

        selected_entity_id = int(input("Seleccione el número de la entidad para ver sus atributos (o 0 para salir): "))
        if selected_entity_id == 0:
            return

        selected_entity = tables[selected_entity_id - 1][0]
        cursor.execute(f"SHOW COLUMNS FROM {selected_entity}")
        print(f"Atributos de la entidad {selected_entity}:")
        for column in cursor:
            print(f"- {column[0]} ({column[1]})")
    except mysql.connector.Error as err:
        print(f"Error al listar los atributos de las entidades: {err}")
    finally:
        cursor.close()
        connection.close()

def agregar_entidad_con_atributos():
    nombre_entidad = input("Ingrese el nombre de la entidad: ")
    atributos_input = input("Ingrese los atributos de la entidad (separados por coma): ")
    atributos = atributos_input.split(',')

    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        verificar_entidad_query = f"SHOW TABLES LIKE '{nombre_entidad}'"
        cursor.execute(verificar_entidad_query)
        if cursor.fetchone():
            print(f"La entidad '{nombre_entidad}' ya existe en la base de datos.")
            return

        create_table_query = f"CREATE TABLE {nombre_entidad} (ID INT PRIMARY KEY AUTO_INCREMENT"
        for atributo in atributos:
            create_table_query += f", {atributo.strip()} VARCHAR(50)"
        create_table_query += ")"

        cursor.execute(create_table_query)
        connection.commit()
        print(f"Se ha creado la nueva entidad '{nombre_entidad}' correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al agregar la nueva entidad con atributos: {err}")
    finally:
        cursor.close()
        connection.close()

def generar_informe_pdf():
    ruta_pdf = "Informe.pdf"
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print("Entidades disponibles:")
        for i, (table_name,) in enumerate(tables, 1):
            print(f"{i}. {table_name}")

        selected_entity_id = int(input("Seleccione el número de la entidad que desea mostrar en el informe: "))
        selected_entity = tables[selected_entity_id - 1][0]

        cursor.execute(f"SHOW COLUMNS FROM {selected_entity}")
        columns = [column[0] for column in cursor]

        print(f"Atributos disponibles para la entidad '{selected_entity}':")
        for column in columns:
            print(column)

        selected_attributes_input = input("Ingrese los nombres de los atributos que desea mostrar (separados por coma): ")
        selected_attributes = [attr.strip() for attr in selected_attributes_input.split(',')]

        query = f"SELECT {', '.join(selected_attributes)} FROM {selected_entity}"
        cursor.execute(query)
        data = cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Informe de la entidad: {selected_entity}", ln=True, align='C')

        for row in data:
            for col, val in zip(selected_attributes, row):
                pdf.cell(200, 10, txt=f"{col}: {val}", ln=True, align='L')

        pdf.output(ruta_pdf)
        print(f"Informe PDF generado correctamente: {ruta_pdf}")
    except mysql.connector.Error as err:
        print(f"Error al generar el informe: {err}")
    finally:
        cursor.close()
        connection.close()

def generar_procedimientos_almacenados():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        for (table_name,) in tables:
            sb = []
            sb.append(f"-- Procedimientos almacenados para la tabla {table_name}\n")

            sb.append(f"CREATE PROCEDURE Insertar{table_name}()\n")
            sb.append("BEGIN\n")
            sb.append(f"    INSERT INTO {table_name} ()\n")
            sb.append("    VALUES ();")
            sb.append("END;\n")

            sb.append(f"CREATE PROCEDURE Actualizar{table_name}()\n")
            sb.append("BEGIN\n")
            sb.append(f"    UPDATE {table_name}\n")
            sb.append("    SET ;\n")
            sb.append("    WHERE ;")
            sb.append("END;\n")

            sb.append(f"CREATE PROCEDURE Eliminar{table_name}()\n")
            sb.append("BEGIN\n")
            sb.append(f"    DELETE FROM {table_name}\n")
            sb.append("    WHERE ;")
            sb.append("END;\n")

            sb.append(f"CREATE PROCEDURE Seleccionar{table_name}()\n")
            sb.append("BEGIN\n")
            sb.append(f"    SELECT * FROM {table_name};")
            sb.append("END;\n")

            print("\n".join(sb))
    except mysql.connector.Error as err:
        print(f"Error al generar procedimientos almacenados: {err}")
    finally:
        cursor.close()
        connection.close()

def ver_tablas_y_atributos():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        database_name = config['database']  # Asegúrate de que esta clave exista en tu configuración
        query = f"""
        SELECT 
            TABLE_NAME, 
            COLUMN_NAME, 
            DATA_TYPE 
        FROM 
            INFORMATION_SCHEMA.COLUMNS
        WHERE 
            TABLE_SCHEMA = '{database_name}'
        ORDER BY 
            TABLE_NAME, 
            ORDINAL_POSITION
        """
        cursor.execute(query)
        current_table = None
        for (table_name, column_name, data_type) in cursor:
            if current_table != table_name:
                current_table = table_name
                print(f"\nTabla: {table_name}")
                print("-" * 50)
            print(f"{column_name} - {data_type}")
    except mysql.connector.Error as err:
        print(f"Error al obtener las tablas y atributos: {err}")
    except KeyError as key_err:
        print(f"Error en la configuración: clave {key_err} no encontrada en 'config'")
    finally:
        cursor.close()
        connection.close()

# Llamada a la función para ver los resultados
ver_tablas_y_atributos()

def crear_tabla_auditoria():
    nombre_tabla = input("Ingrese el nombre de la tabla de auditoría: ")
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = f"""
        CREATE TABLE IF NOT EXISTS {nombre_tabla} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre_tabla VARCHAR(255),
            operacion VARCHAR(10),
            usuario_actual VARCHAR(255),
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            detalle_anterior TEXT,
            detalle_nuevo TEXT
        );
        """
        cursor.execute(query)
        connection.commit()
        print(f"Tabla '{nombre_tabla}' creada correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al crear la tabla '{nombre_tabla}': {err}")
    finally:
        cursor.close()
        connection.close()

def generar_triggers_auditoria(nombre_tabla):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Verificar si la tabla especificada existe
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if (nombre_tabla,) not in tables:
            print(f"La tabla '{nombre_tabla}' no existe en la base de datos.")
            return

        if nombre_tabla == 'auditoria':
            print("No se puede generar triggers para la tabla 'auditoria'.")
            return

        cursor.execute(f"SHOW COLUMNS FROM {nombre_tabla}")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]

        new_columns = ", ".join([f"NEW.{col}" for col in column_names])
        old_columns = ", ".join([f"OLD.{col}" for col in column_names])

        trigger_insert = f"""
        CREATE TRIGGER {nombre_tabla}_AFTER_INSERT AFTER INSERT ON {nombre_tabla}
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (nombre_tabla, operacion, usuario_actual, detalle_nuevo)
            VALUES ('{nombre_tabla}', 'INSERT', USER(), CONCAT_WS(',', {new_columns}));
        END;
        """
        
        trigger_update = f"""
        CREATE TRIGGER {nombre_tabla}_AFTER_UPDATE AFTER UPDATE ON {nombre_tabla}
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (nombre_tabla, operacion, usuario_actual, detalle_anterior, detalle_nuevo)
            VALUES ('{nombre_tabla}', 'UPDATE', USER(), CONCAT_WS(',', {old_columns}), CONCAT_WS(',', {new_columns}));
        END;
        """
        
        trigger_delete = f"""
        CREATE TRIGGER {nombre_tabla}_AFTER_DELETE AFTER DELETE ON {nombre_tabla}
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (nombre_tabla, operacion, usuario_actual, detalle_anterior)
            VALUES ('{nombre_tabla}', 'DELETE', USER(), CONCAT_WS(',', {old_columns}));
        END;
        """

        # Ejecutar los triggers en la base de datos
        cursor.execute(trigger_insert)
        cursor.execute(trigger_update)
        cursor.execute(trigger_delete)
        
        # Crear un directorio para guardar los archivos SQL si no existe
        ruta_guardado = r'C:\Users\Usuario\Desktop\segudon paracil tutoria\Proyecto de Gestion Talento Humano\disparadores'
        os.makedirs(ruta_guardado, exist_ok=True)
        
        # Guardar los triggers en archivos SQL
        with open(os.path.join(ruta_guardado, f'{nombre_tabla}_AFTER_INSERT.sql'), 'w') as file:
            file.write(trigger_insert)
        with open(os.path.join(ruta_guardado, f'{nombre_tabla}_AFTER_UPDATE.sql'), 'w') as file:
            file.write(trigger_update)
        with open(os.path.join(ruta_guardado, f'{nombre_tabla}_AFTER_DELETE.sql'), 'w') as file:
            file.write(trigger_delete)

        connection.commit()
        print(f"Triggers de auditoría generados y guardados en archivos SQL para la tabla '{nombre_tabla}'.")

    except mysql.connector.Error as err:
        print(f"Error al generar triggers de auditoría: {err}")
    finally:
        cursor.close()
        connection.close()
filtros = []

def gestionar_logs_eventos_auditoria():
    while True:
        print("\nGestión de Logs de Eventos y Auditoría")
        print("1. Acceder a logs de eventos y auditoría")
        print("2. Agregar filtros")
        print("3. Generar informe PDF con información filtrada")
        print("4. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion.isdigit():
            opcion = int(opcion)
            if opcion == 1:
                acceder_logs()
            elif opcion == 2:
                agregar_filtros()
            elif opcion == 3:
                generar_informe_pdf_filtrado()
            elif opcion == 4:
                return
            else:
                print("Opción no válida.")
        else:
            print("Por favor, ingrese un número válido.")

def acceder_logs():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        query = "SELECT * FROM auditoria"
        if filtros:
            query += " WHERE " + " AND ".join(filtros)
        cursor.execute(query)

        rows = cursor.fetchall()
        if not rows:
            print("No se encontraron registros con los filtros aplicados.")
        else:
            for row in rows:
                print(f"ID: {row[0]}, Tabla: {row[1]}, Operación: {row[2]}, Usuario: {row[3]}, Fecha: {row[4]}, Detalle Anterior: {row[5]}, Detalle Nuevo: {row[6]}")
    except mysql.connector.Error as err:
        print(f"Error al acceder a los logs: {err}")
    finally:
        cursor.close()
        connection.close()

def agregar_filtros():
    filtro = input("Ingrese el filtro en formato SQL (ejemplo: operacion = 'INSERT'): ")

    if validar_filtro(filtro):
        filtros.append(filtro)
        print("Filtro agregado correctamente.")
    else:
        print("Filtro no válido. Por favor, ingrese un filtro en formato SQL correcto.")

def validar_filtro(filtro):
    valid_columns = ["id", "nombre_tabla", "operacion", "usuario_actual", "fecha_hora", "detalle_anterior", "detalle_nuevo"]
    filtro_parts = filtro.split('=')

    if len(filtro_parts) == 2 and filtro_parts[0].strip() in valid_columns:
        return True

    return False

def generar_informe_pdf_filtrado():
    global filtros
    ruta_pdf = "InformeLogsFiltrados.pdf"
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        query = "SELECT * FROM auditoria"
        if filtros:
            query += " WHERE " + " AND ".join(filtros)
        print(f"Ejecutando consulta: {query}")  # Agregar depuración
        cursor.execute(query)
        data = cursor.fetchall()

        pdf = FPDF('L', 'mm', 'A4')  # 'L' indica orientación Landscape (horizontal)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(275, 10, txt="Informe de Logs de Eventos y Auditoría (Filtrado)", ln=True, align='C')
        pdf.cell(275, 10, txt=f"Fecha de generación: {datetime.now()}", ln=True, align='C')
        pdf.cell(275, 10, txt=f"Filtros aplicados: {', '.join(filtros)}", ln=True, align='C')
        pdf.ln(10)

        headers = ["ID", "Tabla", "Operación", "Usuario", "Fecha", "Detalle Anterior", "Detalle Nuevo"]
        cell_widths = [10, 30, 20, 20, 40, 75, 75]  # Ajusta los anchos de las celdas según sea necesario

        for i, header in enumerate(headers):
            pdf.cell(cell_widths[i], 10, txt=header, ln=False, align='C')
        pdf.ln(10)

        for row in data:
            for i, item in enumerate(row):
                pdf.cell(cell_widths[i], 10, txt=str(item), ln=False, align='C')
            pdf.ln(10)

        pdf.output(ruta_pdf)
        print(f"Informe PDF generado correctamente: {ruta_pdf}")
    except mysql.connector.Error as err:
        print(f"Error al generar el informe PDF: {err}")
    finally:
        cursor.close()
        connection.close()


def generar_informe_o_descargar_triggers():
    print("1. Generar informe PDF de tabla")
    print("2. Descargar triggers")
    opcion = int(input("Seleccione una opción: "))

    if opcion == 1:
        try:
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            print("Tablas disponibles:")
            for i, (table_name,) in enumerate(tables, 1):
                print(f"{i}. {table_name}")

            seleccion = int(input("Seleccione el número de la tabla para generar el informe: "))
            tabla_seleccionada = tables[seleccion - 1][0]

            query = f"SELECT * FROM {tabla_seleccionada}"
            cursor.execute(query)
            data = cursor.fetchall()

            cursor.execute(f"SHOW COLUMNS FROM {tabla_seleccionada}")
            columns = [column[0] for column in cursor]

            ruta_pdf = f"Informe_{tabla_seleccionada}.pdf"
            pdf = FPDF('L', 'mm', 'A4')
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt=f"Informe de la tabla: {tabla_seleccionada}", ln=True, align='C')
            pdf.cell(0, 10, txt=f"Fecha de generación: {datetime.now()}", ln=True, align='C')
            pdf.ln(10)

            # Definir anchos de columna que ocupen toda la página
            page_width = pdf.w - 2 * pdf.l_margin
            col_widths = [page_width / len(columns)] * len(columns)
            
            # Encabezados de la tabla
            for col, width in zip(columns, col_widths):
                pdf.cell(width, 10, col, border=1, align='C')
            pdf.ln(10)

            # Datos de la tabla
            pdf.set_font("Arial", size=10)
            line_height = pdf.font_size * 2.5
            for row in data:
                x_start = pdf.get_x()
                y_start = pdf.get_y()
                max_y = y_start

                for datum, width in zip(row, col_widths):
                    x_pos = pdf.get_x()
                    pdf.multi_cell(width, line_height, str(datum), border=1, align='C')
                    max_y = max(max_y, pdf.get_y())
                    pdf.set_xy(x_pos + width, y_start)

                pdf.set_xy(x_start, max_y)
                pdf.ln(line_height)

            pdf.output(ruta_pdf)
            print(f"Informe PDF generado: {ruta_pdf}")
        except mysql.connector.Error as err:
            print(f"Error al generar el informe PDF: {err}")
        finally:
            cursor.close()
            connection.close()
    elif opcion == 2:
        try:
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            query = """
            SELECT 
                TRIGGER_NAME, 
                EVENT_OBJECT_TABLE, 
                ACTION_STATEMENT 
            FROM 
                INFORMATION_SCHEMA.TRIGGERS
            """
            cursor.execute(query)
            triggers = cursor.fetchall()

            triggers_sql = []
            for trigger in triggers:
                triggers_sql.append(f"-- Trigger: {trigger[0]} on table {trigger[1]}")
                triggers_sql.append(trigger[2])
                triggers_sql.append("DELIMITER ;")

            ruta_archivo = os.path.join(os.path.expanduser('~'), 'Downloads', 'triggers_all_tables.sql')
            with open(ruta_archivo, 'w') as f:
                f.write("\n".join(triggers_sql))

            print(f"Triggers descargados en: {ruta_archivo}")
        except mysql.connector.Error as err:
            print(f"Error al descargar los triggers: {err}")
        finally:
            cursor.close()
            connection.close()
            
if __name__ == "__main__":
    main()
