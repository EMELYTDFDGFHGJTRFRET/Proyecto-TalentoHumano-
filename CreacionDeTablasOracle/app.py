import os
from flask import Flask, render_template, request, redirect, url_for, make_response, flash
import datetime
import cx_Oracle
import subprocess
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from reportlab.pdfgen import canvas

UPLOAD_FOLDER = 'C:\\backups\\'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '123456789'


dsn = cx_Oracle.makedsn("localhost", 1521, sid="xe")
conn = cx_Oracle.connect(user="db_curso", password="12345", dsn=dsn)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']
        try:
            cursor = conn.cursor()
            cursor.execute(f"CREATE USER {nombre_usuario} IDENTIFIED BY {contraseña}")
            cursor.execute(f"GRANT CONNECT TO {nombre_usuario}")
            conn.commit()
            flash(f"Usuario '{nombre_usuario}' creado exitosamente", "success")
        except cx_Oracle.Error as error:
            flash(f"Error al crear usuario: {error}", "danger")
        finally:
            if cursor:
                cursor.close()
            return redirect(url_for('index'))
    return render_template('crear_usuario.html')

@app.route('/modificar_usuario', methods=['GET', 'POST'])
def modificar_usuario():
    if request.method == 'POST':
        nuevo_nombre_usuario = request.form['nuevo_nombre_usuario'].strip()
        nombre_usuario_actual = request.form['nombre_usuario_actual'].strip()

        if nuevo_nombre_usuario and nombre_usuario_actual:
            try:
                cursor = conn.cursor()
                cursor.execute(f"ALTER USER {nombre_usuario_actual} RENAME TO {nuevo_nombre_usuario}")
                conn.commit()
                flash(f"Usuario '{nombre_usuario_actual}' modificado exitosamente a '{nuevo_nombre_usuario}'", "success")
                return redirect(url_for('index'))
            except cx_Oracle.Error as error:
                flash(f"Error al modificar usuario: {error}", "danger")
            finally:
                if cursor:
                    cursor.close()
        else:
            flash("Debes completar ambos campos para modificar un usuario.", "danger")
    return render_template('modificar_usuario.html')

@app.route('/eliminar_usuario', methods=['GET', 'POST'])
def eliminar_usuario():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        try:
            cursor = conn.cursor()
            cursor.execute(f"DROP USER {nombre_usuario} CASCADE")
            conn.commit()
            flash(f"Usuario '{nombre_usuario}' eliminado exitosamente", "success")
        except cx_Oracle.Error as error:
            flash(f"Error al eliminar usuario: {error}", "danger")
        finally:
            if cursor:
                cursor.close()
            return redirect(url_for('index'))
    return render_template('eliminar_usuario.html')

@app.route('/crear_rol', methods=['GET', 'POST'])
def crear_rol():
    if request.method == 'POST':
        nombre_rol = request.form['nombre_rol']
        try:
            cursor = conn.cursor()
            cursor.execute(f"CREATE ROLE {nombre_rol}")
            conn.commit()
            flash(f"Rol '{nombre_rol}' creado con éxito", "success")
        except cx_Oracle.Error as e:
            flash(f"Error al crear el rol: {e}", "danger")
        finally:
            if cursor:
                cursor.close()
        return redirect(url_for('crear_rol'))
    return render_template('crear_rol.html')

@app.route('/asignar_rol', methods=['GET', 'POST'])
def asignar_rol():
    if request.method == 'POST':
        nombre_rol = request.form['nombre_rol']
        nombre_usuario = request.form['nombre_usuario']
        try:
            cursor = conn.cursor()
            cursor.execute(f"GRANT {nombre_rol} TO {nombre_usuario}")
            conn.commit()
            flash(f"Rol '{nombre_rol}' asignado al usuario '{nombre_usuario}' con éxito", "success")
        except cx_Oracle.Error as e:
            flash(f"Error al asignar el rol: {e}", "danger")
        finally:
            if cursor:
                cursor.close()
        return redirect(url_for('index'))
    return render_template('asignar_rol.html')

@app.route('/listar_usuarios', methods=['GET'])
def listar_usuarios():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM all_users ORDER BY username")
        usuarios = cursor.fetchall()
        return render_template('listar_usuarios.html', usuarios=usuarios)
    except cx_Oracle.Error as error:
        flash(f"Error al obtener la lista de usuarios: {error}", "danger")
        return "Error al obtener la lista de usuarios"
    finally:
        if cursor:
            cursor.close()

@app.route('/listar_roles')
def listar_roles():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM dba_roles ORDER BY role")
        roles = cursor.fetchall()
        return render_template('listar_roles.html', roles=roles)
    except cx_Oracle.Error as e:
        flash(f"Error al obtener la lista de roles: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
    return "Error al listar roles"

@app.route('/respaldar_bd', methods=['GET', 'POST'])
def respaldar_bd():
    if request.method == 'POST':
        nombre_bd = 'G_Academica'
        ruta_respaldo = 'C:\\backups\\'
        if not os.path.exists(ruta_respaldo):
            os.makedirs(ruta_respaldo)
        nombre_archivo = nombre_bd + datetime.datetime.now().strftime("_%Y%m%d%H%M%S") + '.dmp'
        ruta_completa = os.path.join(ruta_respaldo, nombre_archivo)
        
        print(f"Intentando guardar el respaldo en: {ruta_completa}")
        cmd = [
            "expdp", "system/admin123",
            f"schemas={nombre_bd}",
            f"directory=DATA_PUMP_DIR",
            f"dumpfile={nombre_archivo}",
            f"LOGFILE={nombre_bd}_backup.log"
        ]
        try:
            result = subprocess.run(cmd, check=True, text=True, capture_output=True)
            return f'Respaldo realizado con éxito en {ruta_completa}'
        except subprocess.CalledProcessError as e:
            return f'Error al realizar el respaldo: {e.stderr}'
        
    return render_template('respaldar_bd.html')

@app.route('/restaurar_bd', methods=['GET', 'POST'])
def restaurar_bd():
    if request.method == 'POST':
        if 'restaurar' in request.form:
            archivo_bak = request.files['archivo_bak']
            if archivo_bak.filename == '':
                return 'Error: No se seleccionó ningún archivo para restaurar'

            ruta_archivo_bak = os.path.join('C:\\backups\\', archivo_bak.filename)
            archivo_bak.save(ruta_archivo_bak)

            nombre_bd = 'G_Academica'
            cmd = [
                "impdp", "system/admin123",
                f"schemas={nombre_bd}",
                f"directory=DATA_PUMP_DIR",
                f"dumpfile={archivo_bak.filename}",
                f"LOGFILE={nombre_bd}_restore.log"
            ]
            try:
                result = subprocess.run(cmd, check=True, text=True, capture_output=True)
                return f'Restauración realizada con éxito desde {archivo_bak.filename}'
            except subprocess.CalledProcessError as e:
                return f'Error al realizar la restauración: {e.stderr}'
    return render_template('restaurar_bd.html')

@app.route('/listar_entidades')
def listar_entidades():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM user_tables")
        entidades = cursor.fetchall()
        return render_template('listar_entidades.html', entidades=entidades)
    except cx_Oracle.Error as e:
        flash(f"Error al obtener la lista de entidades: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
    return "Error al establecer conexión con la base de datos"

class EntidadForm(FlaskForm):
    entidad = StringField('Nombre de la entidad', validators=[DataRequired()])
    submit = SubmitField('Listar Atributos')

@app.route('/listar_atributos', methods=['GET', 'POST'])
def listar_atributos():
    form = EntidadForm()
    if form.validate_on_submit():
        entidad = form.entidad.data.strip()
        return redirect(url_for('listar_atributos_entidad', entidad=entidad))
    return render_template('listar_atributos.html', form=form)

@app.route('/listar_atributos/<entidad>')
def listar_atributos_entidad(entidad):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT column_name FROM user_tab_columns WHERE table_name = :1", (entidad.upper(),))
        atributos = cursor.fetchall()
        return render_template('listar_atributos_entidad.html', entidad=entidad, atributos=atributos)
    except cx_Oracle.Error as e:
        flash(f"Error al obtener la lista de atributos de la entidad '{entidad}': {e}", "danger")
    finally:
        if cursor:
            cursor.close()
    return f"Error al establecer conexión con la base de datos o entidad '{entidad}' no encontrada"

def crear_entidad_y_atributos(conn, nombre_entidad, atributos):
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE {nombre_entidad} (id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY)")
        for atributo in atributos:
            cursor.execute(f"ALTER TABLE {nombre_entidad} ADD {atributo} VARCHAR2(255)")
        conn.commit()
        flash(f"Tabla '{nombre_entidad}' creada con éxito junto con sus atributos.", "success")
        return True
    except cx_Oracle.Error as e:
        flash(f"Error al crear la tabla y sus atributos: {e}", "danger")
        return False

@app.route('/crear_tabla', methods=['GET', 'POST'])
def crear_tabla():
    try:
        if request.method == 'POST':
            nombre_tabla = request.form['nombre_tabla']
            atributos_str = request.form['atributos']
            atributos = [attr.strip() for attr in atributos_str.split(',') if attr.strip()]

            if nombre_tabla and atributos:
                if crear_entidad_y_atributos(conn, nombre_tabla, atributos):
                    conn.commit()
                    return redirect(url_for('index'))
                else:
                    return "Error al crear la tabla y sus atributos."
            else:
                return "Debes proporcionar un nombre de tabla y al menos un atributo."

        return render_template('crear_tabla.html')
    except cx_Oracle.Error as e:
        flash(f"Error de base de datos: {e}", "danger")
        return "Error de base de datos."

@app.route('/generar_pdf', methods=['GET', 'POST'])
def generar_pdf():
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM user_tables")
    tablas = cursor.fetchall()

    if request.method == 'POST' and 'atributos_seleccionados' in request.form:
        tabla = request.form['tabla_seleccionada']
        atributos_seleccionados = request.form.getlist('atributos_seleccionados')

        query = f"SELECT {', '.join(atributos_seleccionados)} FROM {tabla}"
        cursor.execute(query)
        data = cursor.fetchall()

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        data_for_table = [atributos_seleccionados]
        for row in data:
            data_for_table.append(list(row))

        table = Table(data_for_table)

        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ])
        table.setStyle(style)

        elems = []

        styles = getSampleStyleSheet()
        title = Paragraph(f"<para align=center spaceb=3><font size=18><b>Datos de la tabla: {tabla}</b></font></para>", styles["BodyText"])
        elems.append(title)

        elems.append(Spacer(1, 20))

        elems.append(table)
        doc.build(elems)
        pdf = buffer.getvalue()
        buffer.close()

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=report.pdf'
        return response

    elif request.method == 'POST':
        tabla_actual = request.form['tabla_seleccionada']
        cursor.execute(f"SELECT column_name FROM user_tab_columns WHERE table_name = '{tabla_actual.upper()}'")
        atributos = cursor.fetchall()
        cursor.close()
        return render_template('generar_pdf.html', tablas=tablas, atributos=atributos, tabla_actual=tabla_actual)

    cursor.close()
    return render_template('generar_pdf.html', tablas=tablas)

@app.route('/generar_procedimientos', methods=['GET', 'POST'])
def generar_procedimientos():
    if request.method == 'POST':
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT table_name FROM user_tables")
            table_names = [row[0] for row in cursor.fetchall()]

            for table_name in table_names:
                cursor.execute(f"""
                SELECT column_name
                FROM all_cons_columns
                WHERE constraint_name = (
                    SELECT constraint_name
                    FROM user_constraints
                    WHERE table_name = '{table_name.upper()}' AND constraint_type = 'P'
                )
                """)
                primary_key_column = cursor.fetchone()[0]

                cursor.execute(f"""
                SELECT column_name, data_type
                FROM user_tab_columns
                WHERE table_name = '{table_name.upper()}'
                """)
                columns = cursor.fetchall()

                columns_list = []
                columns_list_params = []
                for column in columns:
                    col_name = column[0]
                    col_type = column[1]

                    if col_name != primary_key_column:
                        columns_list.append(f'"{col_name}"')
                        columns_list_params.append(f'{col_name} IN {col_type}')

                columns_list_params.append(f'{primary_key_column} IN NUMBER')

                columns_list_str = ', '.join(columns_list)
                columns_list_params_str = ', '.join(columns_list_params)

                sp_statements = []

                sp_statements.append(f"""
                CREATE OR REPLACE PROCEDURE Insertar{table_name}(
                    {columns_list_params_str}
                ) AS
                BEGIN
                    INSERT INTO {table_name} ({columns_list_str}, "{primary_key_column}")
                    VALUES ({', '.join(':' + col for col in columns_list)}, :{primary_key_column});
                END;
                """)

                update_set_clause = ', '.join(f'"{col}" = :{col}' for col in columns_list)
                sp_statements.append(f"""
                CREATE OR REPLACE PROCEDURE Actualizar{table_name}(
                    {columns_list_params_str}
                ) AS
                BEGIN
                    UPDATE {table_name}
                    SET {update_set_clause}
                    WHERE "{primary_key_column}" = :{primary_key_column};
                END;
                """)

                sp_statements.append(f"""
                CREATE OR REPLACE PROCEDURE Eliminar{table_name}(
                    {primary_key_column} IN NUMBER
                ) AS
                BEGIN
                    DELETE FROM {table_name}
                    WHERE "{primary_key_column}" = :{primary_key_column};
                END;
                """)

                sp_statements.append(f"""
                CREATE OR REPLACE PROCEDURE Seleccionar{table_name}(cursor OUT SYS_REFCURSOR) AS
                BEGIN
                    OPEN cursor FOR SELECT * FROM {table_name};
                END;
                """)

                for sp_statement in sp_statements:
                    cursor.execute(sp_statement)
                    conn.commit()

            flash("Procedimientos almacenados generados con éxito", "success")
        except cx_Oracle.Error as e:
            flash(f"Error al generar procedimientos almacenados: {e}", "danger")
        finally:
            if cursor:
                cursor.close()
    return render_template('generar_procedimientos.html')

@app.route('/eliminar_procedimientos', methods=['POST'])
def eliminar_procedimientos():
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT object_name
        FROM user_procedures
        WHERE object_type = 'PROCEDURE' AND
              (
                  object_name LIKE 'Insertar%' OR
                  object_name LIKE 'Actualizar%' OR
                  object_name LIKE 'Eliminar%' OR
                  object_name LIKE 'Seleccionar%'
              )
        """)
        proc_names = [row[0] for row in cursor.fetchall()]
        
        for proc_name in proc_names:
            cursor.execute(f"DROP PROCEDURE {proc_name}")
            conn.commit()
            print(f"Procedimiento eliminado: {proc_name}")

        flash("Procedimientos almacenados eliminados con éxito", "success")
    except cx_Oracle.Error as e:
        flash(f"Error al eliminar procedimientos almacenados: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
    return render_template('eliminar_procedimientos.html')

if __name__ == '__main__':
    app.run(debug=True)
