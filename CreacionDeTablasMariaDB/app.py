import mysql.connector
from mysql.connector import connect, Error
import subprocess
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas


def limpiar_pantalla():
    # Clear screen command based on the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')
        
def mostrar_menu():
    print("\nMenu de Opciones:")
    print("1. Crear usuario en la base de datos")
    print("2. Lista de usuarios en la base de datos")
    print("3. Modificar un usuario")
    print("4. Eliminar un usuario")
    print("5. Crear un rol")
    print("6. Lista de Roles")
    print("7. Asignar un rol a un usuario")
    print("8. Respaldar base de datos")
    print("9. Restaurar base de datos")
    print("10. Generar PDF")
    print("11. CRUD")
    print("20. Salir")

# Crear usuario
def crear_usuario_mariadb(cursor, nombre_usuario, contraseña):
    try:
        query = "CREATE USER %s@'localhost' IDENTIFIED BY %s"
        cursor.execute(query, (nombre_usuario, contraseña))
        print("Usuario creado exitosamente.")
    except Exception as e:
        
        print(f"Error al crear el usuario: {e}")

def opcion1(cursor):
    limpiar_pantalla()
    print("Ejecutando Opción 1...")
    nombre_usuario = input("Ingrese el nombre del nuevo usuario de la base de datos: ")
    contraseña = input("Ingrese la contraseña para el nuevo usuario: ")
    crear_usuario_mariadb(cursor, nombre_usuario, contraseña)
    input("Presione Enter para regresar al menú principal...")
    limpiar_pantalla()

# Mostrar usuarios 
def mostrar_usuarios(cursor):
    try:
        query = """
        SELECT User FROM mysql.user
        WHERE Host = 'localhost' AND User NOT IN ('mysql.session', 'mysql.sys', 'debian-sys-maint')
        ORDER BY User;
        """
        cursor.execute(query)
        usuarios = cursor.fetchall()
        if usuarios:
            print("Usuarios de la base de datos:")
            for index, usuario in enumerate(usuarios, start=1):
                print(f"{index}. {usuario[0]}")
            return usuarios 
        else:
            print("No hay usuarios disponibles.")
            return []
    except Exception as e:
        print(f"Error al obtener la lista de usuarios: {e}")
        return []

def opcion2(cursor):
    limpiar_pantalla()
    print("Ejecutando Opción 2...")
    mostrar_usuarios(cursor)
    input("Presione Enter para regresar al menú principal...")
    limpiar_pantalla()

# Modificar usuarios
def cambiar_nombre_usuario(cursor, nombre_actual, nuevo_nombre):
    try:
        query = "RENAME USER %s@'localhost' TO %s@'localhost'"
        cursor.execute(query, (nombre_actual, nuevo_nombre))
        print("Nombre de usuario cambiado exitosamente.")
    except Exception as e:
        print(f"Error al cambiar el nombre del usuario: {e}")

def cambiar_contraseña_usuario(cursor, nombre_usuario, nueva_contraseña):
    try:
        query = "ALTER USER %s@'localhost' IDENTIFIED BY %s"
        cursor.execute(query, (nombre_usuario, nueva_contraseña))
        print("Contraseña cambiada exitosamente.")
    except Exception as e:
        print(f"Error al cambiar la contraseña del usuario: {e}")

def opcion3(cursor):
    limpiar_pantalla()
    print("Ejecutando Opción 3...")
    usuarios = mostrar_usuarios(cursor)
    if usuarios:
        try:
            eleccion = int(input("Seleccione el número del usuario a modificar: "))
            nombre_actual = usuarios[eleccion - 1][0] 
            nuevo_nombre = input("Ingrese el nuevo nombre del usuario: ")
            nueva_contraseña = input("Ingrese la nueva contraseña del usuario: ")
            
            cambiar_nombre_usuario(cursor, nombre_actual, nuevo_nombre)
            cambiar_contraseña_usuario(cursor, nuevo_nombre, nueva_contraseña)  
        except ValueError:
            print("Por favor, ingrese un número válido.")
        except IndexError:
            print("Selección no válida. Por favor, elija un número de la lista.")
    else:
        print("No hay usuarios para modificar.")
    input("Presione Enter para regresar al menú principal...")
    limpiar_pantalla()

# Eliminar usuarios
def eliminar_usuario_mariadb(cursor, nombre_usuario):
    try:
        query = "DROP USER %s@'localhost'"
        cursor.execute(query, (nombre_usuario,))
        print("Usuario eliminado exitosamente.")
    except Exception as e:
        print(f"Error al eliminar el usuario: {e}")

def opcion4(cursor):
    limpiar_pantalla()
    print("Ejecutando Opción 4...")
    usuarios = mostrar_usuarios(cursor)
    if usuarios:
        try:
            eleccion = int(input("Seleccione el número del usuario a eliminar: "))
            nombre_usuario = usuarios[eleccion - 1][0]  
            confirmacion = input(f"Está seguro de que desea eliminar al usuario '{nombre_usuario}'? (s/n): ")
            if confirmacion.lower() == 's':
                eliminar_usuario_mariadb(cursor, nombre_usuario)
            else:
                print("Eliminación cancelada.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
        except IndexError:
            print("Selección no válida. Por favor, elija un número de la lista.")
    else:
        print("No hay usuarios para eliminar.")
    input("Presione Enter para regresar al menú principal...")
    limpiar_pantalla()

# Crear un rol 
def crear_rol_mariadb(cursor, nombre_rol):
    try:
        query = "CREATE ROLE %s"
        cursor.execute(query, (nombre_rol,))
        print(f"Rol '{nombre_rol}' creado exitosamente.")
    except Exception as e:
        print(f"Error al crear el rol: {e}")

def opcion5(cursor):
    limpiar_pantalla()
    print("Ejecutando Opción 5...")
    nombre_rol = input("Ingrese el nombre del nuevo rol: ")
    crear_rol_mariadb(cursor, nombre_rol)
    input("Presione Enter para regresar al menú principal...")
    limpiar_pantalla()

# Mostrar roles
def mostrar_roles(cursor):
    try:
        cursor.execute("SELECT User FROM mysql.user WHERE Is_role = 'Y'")
        roles = cursor.fetchall()
        if roles:
            print("Roles disponibles en la base de datos:")
            for index, rol in enumerate(roles, start=1):
                print(f"{index}. {rol[0]}")
            return roles
        else:
            print("No hay roles disponibles.")
            return []
    except Exception as e:
        print(f"Error al obtener la lista de roles: {e}")
        return []

def opcion6(cursor):
    limpiar_pantalla()
    print("Ejecutando Opción 6...")
    mostrar_roles(cursor)
    input("Presione Enter para regresar al menú principal...")
    limpiar_pantalla()


# Asignar un rol a un usuario 
def asignar_rol_a_usuario(cursor, nombre_usuario, nombre_rol):
    try:
        query = "GRANT %s TO %s@'localhost'"
        cursor.execute(query, (nombre_rol, nombre_usuario))
        print(f"Rol '{nombre_rol}' asignado exitosamente a '{nombre_usuario}'.")
    except Exception as e:
        print(f"Error al asignar el rol: {e}")

def opcion7(cursor):
    print("Ejecutando Opción 7...")
    usuarios = mostrar_usuarios(cursor)
    if usuarios:
        try:
            seleccion_usuario = int(input("Seleccione el número del usuario al que asignar el rol: ")) - 1
            nombre_usuario = usuarios[seleccion_usuario][0]
        except ValueError:
            print("Por favor, ingrese un número válido.")
            return
        except IndexError:
            print("Selección no válida. Por favor, elija un número de la lista.")
            return

    roles = mostrar_roles(cursor)
    if roles:
        try:
            seleccion_rol = int(input("Seleccione el número del rol a asignar: ")) - 1
            nombre_rol = roles[seleccion_rol][0]
        except ValueError:
            print("Por favor, ingrese un número válido.")
            return
        except IndexError:
            print("Selección no válida. Por favor, elija un número de la lista.")
            return

    asignar_rol_a_usuario(cursor, nombre_usuario, nombre_rol)
    input("Presione Enter para regresar al menú principal...")
    limpiar_pantalla()



#RESPALDO DE BASE DE DATOS
def realizar_respaldo(host, database, user, password, output_dir):
    try:
        # Asegurarse de que el directorio de salida existe, si no, crearlo
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Directorio {output_dir} creado.")
        
        # Generar nombre de archivo basado en la fecha y hora actual
        fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{database}_{fecha_hora}.sql"
        output_path = os.path.join(output_dir, nombre_archivo)

        # Conectar a la base de datos
        with mysql.connector.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=database
        ) as connection:
            cursor = connection.cursor()

            # Escribir estructura y datos de las tablas en el archivo SQL
            with open(output_path, 'w') as file:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SHOW CREATE TABLE {table_name}")
                    create_table_statement = cursor.fetchone()[1]
                    file.write(f"{create_table_statement};\n\n")
                    cursor.execute(f"SELECT * FROM {table_name}")
                    for row in cursor:
                        values = ", ".join([f"'{str(value)}'" if value is not None else "NULL" for value in row])
                        file.write(f"INSERT INTO {table_name} VALUES {row};\n")
                    file.write("\n")

            print(f"Respaldo realizado exitosamente en {output_path}")

    except mysql.connector.Error as e:
        print(f"Error al realizar el respaldo: {e}")

def opcion8(cursor):
    print("Ejecutando Opción 8...")
    host = "localhost"
    database = "mariadb"
    user = "root"
    password = "Evelyn123"
    output_dir = r"c:\Users\HP\OneDrive\Escritorio\MARIADB\respaldo"
    realizar_respaldo(host, database, user, password, output_dir)
    input("Presione Enter para regresar al menú principal...")
    limpiar_pantalla()


#RESPALDO DE BASE DE DATOS
def listar_archivos_de_respaldo(directorio_respaldo):
    archivos = [f for f in os.listdir(directorio_respaldo) if f.endswith('.sql')]
    if archivos:
        print("Archivos de respaldo disponibles:")
        for idx, archivo in enumerate(archivos, start=1):
            print(f"{idx}. {archivo}")
    else:
        print("No hay archivos de respaldo disponibles.")
    return archivos

def eliminar_todas_las_tablas(cursor):
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        print("Todas las tablas han sido eliminadas.")
    except mysql.connector.Error as e:
        print(f"Error al eliminar las tablas: {e}")

def realizar_restauracion(host, database, user, password, respaldo_path):
    try:
        with open(respaldo_path, 'r') as file:
            sql_script = file.read()
        
        # Conectar a la base de datos
        with mysql.connector.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=database
        ) as connection:
            cursor = connection.cursor()
            
            # Eliminar todas las tablas existentes
            eliminar_todas_las_tablas(cursor)
            
            # Deshabilitar las restricciones de clave foránea
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # Separar las sentencias SQL
            sql_commands = sql_script.split(';')
            
            # Ejecutar cada consulta individual
            for command in sql_commands:
                if command.strip():  # Ignorar comandos vacíos
                    try:
                        cursor.execute(command)
                    except mysql.connector.Error as e:
                        print(f"Error al ejecutar el comando: {e}")
                        continue
            
            # Habilitar las restricciones de clave foránea
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        print(f"Base de datos restaurada exitosamente desde {respaldo_path} a la base de datos {database}")
    except mysql.connector.Error as e:
        print(f"Error al restaurar la base de datos: {e}")

def listar_bases_de_datos(host, user, password):
    try:
        # Conectar al servidor de la base de datos
        with mysql.connector.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
        ) as connection:
            # Obtener el cursor
            cursor = connection.cursor()
            # Ejecutar la consulta para obtener todas las bases de datos
            cursor.execute("SHOW DATABASES")
            # Obtener y retornar la lista de bases de datos
            return [database[0] for database in cursor.fetchall()]
    except mysql.connector.Error as e:
        print(f"Error al listar bases de datos: {e}")
        return []

def crear_base_de_datos(host, user, password, database):
    try:
        # Conectar al servidor de la base de datos
        with mysql.connector.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
        ) as connection:
            cursor = connection.cursor()
            # Crear la nueva base de datos
            cursor.execute(f"CREATE DATABASE {database}")
            print(f"Base de datos {database} creada exitosamente.")
    except mysql.connector.Error as e:
        print(f"Error al crear la base de datos: {e}")

def opcion9(cursor):
    while True:
        limpiar_pantalla()
        print("Ejecutando Opción 9...")
        directorio_respaldo = r"c:\Users\HP\OneDrive\Escritorio\MARIADB\respaldo"
        archivos = listar_archivos_de_respaldo(directorio_respaldo)
        if archivos:
            try:
                seleccion = int(input("Seleccione el número del archivo de respaldo a restaurar: ")) - 1
                respaldo_path = os.path.join(directorio_respaldo, archivos[seleccion])
                
                bases_de_datos = listar_bases_de_datos("localhost", "root", "Evelyn123")
                if bases_de_datos:
                    print("Bases de datos disponibles:")
                    for idx, db in enumerate(bases_de_datos, start=1):
                        print(f"{idx}. {db}")
                    print(f"{idx+1}. Crear nueva base de datos")
                    seleccion_db = int(input("Seleccione el número de la base de datos a restaurar o ingrese el número de la opción para crear una nueva: "))
                    if seleccion_db <= idx:
                        nueva_db = bases_de_datos[seleccion_db - 1]
                    else:
                        nueva_db = input("Ingrese el nombre para la nueva base de datos: ")
                        crear_base_de_datos("localhost", "root", "Evelyn123", nueva_db)
                    
                    realizar_restauracion("localhost", nueva_db, "root", "adonis2001", respaldo_path)
                else:
                    print("No hay bases de datos disponibles.")
            except IndexError:
                print("Selección no válida. Por favor, elija un número de la lista.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
            except Exception as e:
                print(f"Error: {e}")
        
        # Opción para realizar una nueva restauración o regresar al inicio
        decision = input("¿Desea realizar otra restauración? (s/n): ").strip().lower()
        if decision != 's':
            break
    input("Presione Enter para regresar al menú principal...")
    limpiar_pantalla()


 #GENERAR PDF
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def obtener_datos_tabla(cursor, tabla, columnas):
    try:
        columnas_sql = ", ".join(columnas)
        query = f"SELECT {columnas_sql} FROM {tabla}"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener datos de la tabla {tabla}: {e}")
        return []

def generar_pdf_con_datos(tabla, datos, columnas, output_dir):
    try:
        # Generar un nombre de archivo único basado en la fecha y hora actuales
        fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"{tabla}_informe_{fecha_hora}.pdf")

        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []

        # Encabezados de la tabla
        data = [columnas]

        # Agregar los datos de la tabla
        for fila in datos:
            data.append([str(dato) for dato in fila])

        # Crear la tabla con los datos
        t = Table(data)

        # Estilos de la tabla
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ]))

        story.append(t)
        doc.build(story)
        print(f"Informe generado en: {output_path}")
    except Exception as e:
        print(f"Error al generar el PDF: {e}")

def obtener_detalles_tablas(cursor, database):
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        tablas = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            tablas[table_name] = [col[0] for col in columns]
        return tablas
    except Exception as e:
        print(f"Error al obtener detalles de las tablas: {e}")
        return {}

def opcion10(cursor):
    database = 'mariadb'
    print("Ejecutando Opción 10...")
    tablas = obtener_detalles_tablas(cursor, database)
    if not tablas:
        print("No se encontraron tablas disponibles.")
        return

    while True:
        print("Tablas disponibles:")
        for idx, tabla in enumerate(tablas.keys(), 1):
            print(f"{idx}. {tabla}")

        idx_tabla = int(input("Seleccione el número de la tabla: ")) - 1
        if idx_tabla < 0 or idx_tabla >= len(tablas):
            print("Selección de tabla inválida.")
            continue
        tabla_seleccionada = list(tablas.keys())[idx_tabla]

        print("Columnas disponibles en", tabla_seleccionada, ":")
        for idx, col in enumerate(tablas[tabla_seleccionada], 1):
            print(f"{idx}. {col}")

        idxs_columnas = input("Seleccione los números de las columnas (dejar en blanco para seleccionar todas): ")
        if not idxs_columnas.strip():
            columnas_seleccionadas = tablas[tabla_seleccionada]
        else:
            columnas_seleccionadas = [tablas[tabla_seleccionada][int(i) - 1] for i in idxs_columnas.split(",")]

        datos = obtener_datos_tabla(cursor, tabla_seleccionada, columnas_seleccionadas)

        output_dir = r"c:\Users\HP\OneDrive\Escritorio\MARIADB\informe"
        generar_pdf_con_datos(tabla_seleccionada, datos, columnas_seleccionadas, output_dir)

        if input("¿Desea agregar otra tabla? (s/n): ").lower() != 's':
            break
    limpiar_pantalla()

 #PROCEDIMIENTO ALMACENADO
import os


def obtener_datos_tabla(cursor, tabla, columnas):
    try:
        columnas_sql = ", ".join(columnas)
        query = f"SELECT {columnas_sql} FROM {tabla}"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener datos de la tabla {tabla}: {e}")
        return []

def obtener_columnas(cursor, tabla):
    cursor.execute(f"SHOW COLUMNS FROM {tabla}")
    return [row for row in cursor.fetchall()]

def generar_procedimiento_insert(tabla, columnas):
    columnas_insertar = [col for col in columnas if col[1] is None or not col[1].startswith('nextval')]
    cols = ", ".join([col[0] for col in columnas_insertar])
    param_definitions = ", ".join([f"IN p_{col[0]} {col[1]}" for col in columnas_insertar])
    valores = ", ".join([f"p_{col[0]}" for col in columnas_insertar])

    proc_insert = f"""
    DELIMITER $$
    CREATE PROCEDURE {tabla}_insert({param_definitions})
    BEGIN
        INSERT INTO {tabla} ({cols}) VALUES ({valores});
    END$$
    DELIMITER ;
    """
    return proc_insert

def generar_procedimiento_select(tabla):
    proc_select = f"""
    DELIMITER $$
    CREATE PROCEDURE {tabla}_select()
    BEGIN
        SELECT * FROM {tabla};
    END$$
    DELIMITER ;
    """
    return proc_select

def generar_procedimiento_update(tabla, columnas, id_column):
    columnas_update = [col for col in columnas if col[0] != id_column]
    param_definitions = ", ".join([f"IN p_{col[0]} {col[1]}" for col in columnas_update])
    set_values = ", ".join([f"{col[0]} = p_{col[0]}" for col in columnas_update])

    proc_update = f"""
    DELIMITER $$
    CREATE PROCEDURE {tabla}update({param_definitions}, IN p{id_column} INT)
    BEGIN
        UPDATE {tabla} SET {set_values} WHERE {id_column} = p_{id_column};
    END$$
    DELIMITER ;
    """
    return proc_update

def generar_procedimiento_delete(tabla, id_column):
    proc_delete = f"""
    DELIMITER $$
    CREATE PROCEDURE {tabla}delete(IN p{id_column} INT)
    BEGIN
        DELETE FROM {tabla} WHERE {id_column} = p_{id_column};
    END$$
    DELIMITER ;
    """
    return proc_delete

def generar_procedimientos_crud(cursor, tabla, columnas, id_column):
    try:
        procedimientos_dir = r"c:\Users\HP\OneDrive\Escritorio\MARIADB\procedimientos"
        if not os.path.exists(procedimientos_dir):
            os.makedirs(procedimientos_dir)

        with open(os.path.join(procedimientos_dir, f"{tabla}_crud.sql"), "w") as f:
            f.write(generar_procedimiento_insert(tabla, columnas))
            f.write("\n")
            f.write(generar_procedimiento_select(tabla))
            f.write("\n")
            f.write(generar_procedimiento_update(tabla, columnas, id_column))
            f.write("\n")
            f.write(generar_procedimiento_delete(tabla, id_column))
        print(f"Procedimientos CRUD para la tabla {tabla} creados exitosamente en la carpeta 'procedimientos'.")
    except Exception as e:
        print(f"Error al generar procedimientos CRUD: {e}")


def opcion11(cursor):
    database = 'tienda'
    print("Ejecutando Opción 11...")

    tablas = obtener_detalles_tablas(cursor, database)
    print("Tablas disponibles:")
    for i, tabla in enumerate(tablas, 1):
        print(f"{i}. {tabla}")

    seleccion_tabla = int(input("Seleccione el número de la tabla: ")) - 1
    if seleccion_tabla < 0 or seleccion_tabla >= len(tablas):
        print("Selección de tabla inválida.")
    else:
        tabla_seleccionada_nombre = list(tablas.keys())[seleccion_tabla]
        columnas = obtener_columnas(cursor, tabla_seleccionada_nombre)
        id_column = next((col[0] for col in columnas if 'id' in col[0].lower()), None)
        generar_procedimientos_crud(cursor, tabla_seleccionada_nombre, columnas, id_column)

    input("Presione Enter para regresar al menú principal...")
    limpiar_pantalla()  
        
        
        
        

def main():
    try:
        connection = connect(
            host="localhost",
            port="3306",
            user="root",
            password="Evelyn123",
            database="mariadb",
            auth_plugin='caching_sha2_password' 
        )
        cursor = connection.cursor()

        while True:
            mostrar_menu()
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:
                opcion1(cursor)
            elif opcion == 2:
                opcion2(cursor)
            elif opcion == 3:
                opcion3(cursor)
            elif opcion == 4:
                opcion4(cursor)
            elif opcion == 5:
                opcion5(cursor)
            elif opcion == 6:
                opcion6(cursor)
            elif opcion == 7:
                opcion7(cursor)
            elif opcion == 8:
                opcion8(cursor)
            elif opcion == 9:
                opcion9(cursor)
            elif opcion == 10:
                opcion10(cursor)
            elif opcion == 11:
                opcion11(cursor)
            elif opcion == 20:
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")
                
            connection.commit()

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")

if __name__ == "__main__":
    main()
