//string connectionString = "Server=WINDOWS-MP\\SQLEXPRESS;Database=TalentoHumano;User Id=tu_usuario;Password=contraseña_de_tu_usuario;Integrated Security=True;";
//TalentoHumano: Zambrano Ivania - Tutotia BD 4 "E"

using System;
using System.Data;
using System.Data.SqlClient;
using System.Reflection.Metadata;
using iText.Kernel.Pdf;
using iText.Layout;
using Document = iText.Layout.Document; // Alias para el espacio de nombres iText.Layout.Document

using iText.Layout.Element;
using System.Text;
using iText.Kernel.Colors;
using iText.Layout.Properties;


namespace CRUDUsuariosRoles
{
    class Program
    {
        static string connectionString = "Server=IvaniaZambrano\\SQLEXPRESS;Database=TalentoHumano;Integrated Security=True;";

        static void Main(string[] args)
        {
            while (true)
            {
                Console.WriteLine("");
                Console.WriteLine("Seleccione una opción:");
                Console.WriteLine("1. Crear Usuario");
                Console.WriteLine("2. Modificar Usuario");
                Console.WriteLine("3. Eliminar Usuario");
                Console.WriteLine("4. Crear Rol");
                Console.WriteLine("5. Asignar Rol a Usuario");
                Console.WriteLine("6. Consultar Roles");
                Console.WriteLine("7. Consultar Usuarios");
                Console.WriteLine("8. Realizar respaldo de la base de datos");
                Console.WriteLine("9. Restaurar base de datos");
                Console.WriteLine("10.Listar las entidades");
                Console.WriteLine("11.Listar atributos por entidades");
                Console.WriteLine("12.Agregar entidades con atributos");
                Console.WriteLine("13.Generar reporte en PDF");
                Console.WriteLine("14. Salir");
                Console.WriteLine("15. Procedimientos almacenados");
                Console.WriteLine("");
                Console.WriteLine("");
                Console.WriteLine("--------------------segundo parcial------------------");
                Console.WriteLine("16. Ver todas las tablas y sus atributos");
                Console.WriteLine("17. Crear Tabla de Auditoría");
                Console.WriteLine("18. Generar Triggers de Auditoría");
                Console.WriteLine("19. Gestionar logs de eventos y auditoría");
                Console.WriteLine("20. Generar informe PDF de tabla o descargar triggers");

                Console.WriteLine("");
                Console.Write("Ingrese la opción seleccionada: ");





                int opcion;
                if (!int.TryParse(Console.ReadLine(), out opcion))
                {
                    Console.WriteLine("Opción no válida. Por favor, ingrese un número del 1 al 8.");
                    continue;
                }

                switch (opcion)
                {
                    case 1:
                        CrearLoginYUsuario();
                        break;
                    case 2:
                        ModificarUsuario();
                        break;
                    case 3:
                        EliminarUsuario();
                        break;
                    case 4:
                        CrearRol();
                        break;
                    case 5:
                        AsignarRolUsuario();
                        break;
                    case 6:
                        ConsultarRoles();
                        break;
                    case 7:
                        ConsultarUsuarios();
                        break;
                    case 8:
                        RealizarRespaldo();
                        break;
                    case 9:
                        RestaurarBaseDeDatos();
                        break;
                    case 10:
                        ListarEntidadesBaseDatos();
                        break;
                    case 11:
                        ListarAtributosEntidad();
                        break;
                    case 12:
                        AgregarEntidadConAtributos();
                        break;
                    case 13:
                        GenerarInformePDF();
                        break;
                    case 14:
                        break;
                    case 15:
                        GenerarProcedimientosAlmacenados();
                        return;
                    case 16:
                        VerTablasYAtributos();
                        break;
                    case 17:
                        CrearTablaAuditoria();
                        break;
                    case 18:
                        GenerarTriggersAuditoria();
                        break;
                    case 19:
                        GestionarLogsEventosAuditoria();
                        break;
                    case 20:
                        GenerarInformeODescargarTriggers();
                        break;

                    default:
                        Console.WriteLine("Opción no válida. Por favor, ingrese un número del 1 al 8.");
                        break;
                }
            }
        }

        static void VerTablasYAtributos()
        {
            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();

                    string query = @"
                    SELECT 
                        TABLE_NAME, 
                        COLUMN_NAME, 
                        DATA_TYPE 
                    FROM 
                        INFORMATION_SCHEMA.COLUMNS
                    ORDER BY 
                        TABLE_NAME, 
                        ORDINAL_POSITION";

                    using (SqlCommand command = new SqlCommand(query, connection))
                    using (SqlDataReader reader = command.ExecuteReader())
                    {
                        string currentTable = null;
                        while (reader.Read())
                        {
                            string tableName = reader["TABLE_NAME"].ToString();
                            string columnName = reader["COLUMN_NAME"].ToString();
                            string dataType = reader["DATA_TYPE"].ToString();

                            if (currentTable == null || currentTable != tableName)
                            {
                                currentTable = tableName;
                                Console.WriteLine($"\nTabla: {tableName}");
                                Console.WriteLine(new string('-', 50));
                            }
                            Console.WriteLine($"{columnName} - {dataType}");
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error al obtener las tablas y atributos: {ex.Message}");
            }
        }













        static void GenerarInformeODescargarTriggers()
        {
            while (true)
            {
                Console.WriteLine("\nGenerar informe PDF de tabla o descargar triggers");
                Console.WriteLine("1. Generar informe PDF de una tabla");
                Console.WriteLine("2. Descargar triggers de todas las tablas");
                Console.WriteLine("3. Volver al menú principal");
                Console.Write("Seleccione una opción: ");

                if (int.TryParse(Console.ReadLine(), out int opcion))
                {
                    switch (opcion)
                    {
                        case 1:
                            GenerarInformePDFTabla();
                            break;
                        case 2:
                            DescargarTriggers();
                            break;
                        case 3:
                            return;
                        default:
                            Console.WriteLine("Opción no válida.");
                            break;
                    }
                }
                else
                {
                    Console.WriteLine("Por favor, ingrese un número válido.");
                }
            }
        }

        static void GenerarInformePDFTabla()
        {
            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();

                    // Obtener la lista de tablas
                    List<string> tablas = new List<string>();
                    string queryTablas = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'";
                    using (SqlCommand cmd = new SqlCommand(queryTablas, connection))
                    using (SqlDataReader reader = cmd.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            tablas.Add(reader.GetString(0));
                        }
                    }

                    // Mostrar las tablas disponibles
                    Console.WriteLine("Tablas disponibles:");
                    for (int i = 0; i < tablas.Count; i++)
                    {
                        Console.WriteLine($"{i + 1}. {tablas[i]}");
                    }

                    Console.Write("Seleccione el número de la tabla para generar el informe: ");
                    if (int.TryParse(Console.ReadLine(), out int seleccion) && seleccion > 0 && seleccion <= tablas.Count)
                    {
                        string tablaSeleccionada = tablas[seleccion - 1];

                        // Obtener los datos de la tabla seleccionada
                        string query = $"SELECT * FROM {tablaSeleccionada}";
                        List<Dictionary<string, string>> datos = new List<Dictionary<string, string>>();
                        List<string> columnas = new List<string>();

                        using (SqlCommand cmd = new SqlCommand(query, connection))
                        using (SqlDataReader reader = cmd.ExecuteReader())
                        {
                            // Obtener los nombres de las columnas
                            for (int i = 0; i < reader.FieldCount; i++)
                            {
                                columnas.Add(reader.GetName(i));
                            }

                            // Obtener los datos
                            while (reader.Read())
                            {
                                var fila = new Dictionary<string, string>();
                                foreach (var columna in columnas)
                                {
                                    fila[columna] = reader[columna].ToString();
                                }
                                datos.Add(fila);
                            }
                        }

                        // Generar el informe PDF
                        string rutaPDF = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), $"Informe_{tablaSeleccionada}.pdf");

                        using (PdfWriter writer = new PdfWriter(rutaPDF))
                        using (PdfDocument pdf = new PdfDocument(writer))
                        using (Document document = new Document(pdf, iText.Kernel.Geom.PageSize.A4.Rotate()))
                        {
                            document.SetMargins(20, 20, 20, 20);

                            document.Add(new Paragraph($"Informe de la tabla: {tablaSeleccionada}").SetFontSize(14));
                            document.Add(new Paragraph($"Fecha de generación: {DateTime.Now}").SetFontSize(12));
                            document.Add(new Paragraph("\n"));

                            Table table = new Table(UnitValue.CreatePercentArray(columnas.Count)).UseAllAvailableWidth();
                            table.SetFontSize(10);

                            // Agregar encabezados de columna
                            foreach (var columna in columnas)
                            {
                                table.AddHeaderCell(new Cell().SetBackgroundColor(ColorConstants.LIGHT_GRAY)
                                                              .SetTextAlignment(TextAlignment.CENTER)
                                                              .Add(new Paragraph(columna).SetFontSize(10)));
                            }

                            // Agregar datos de las filas
                            foreach (var fila in datos)
                            {
                                foreach (var columna in columnas)
                                {
                                    table.AddCell(new Cell().SetTextAlignment(TextAlignment.LEFT)
                                                            .Add(new Paragraph(fila[columna]).SetFontSize(8)));
                                }
                            }

                            document.Add(table);
                        }

                        Console.WriteLine($"Informe PDF generado: {rutaPDF}");
                    }
                    else
                    {
                        Console.WriteLine("Selección no válida.");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error al generar el informe PDF: {ex.Message}");
            }
        }

        static void DescargarTriggers()
        {
            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();

                    StringBuilder allTriggers = new StringBuilder();

                    string queryTriggers = @"
                SELECT 
                    t.name AS TriggerName,
                    OBJECT_NAME(t.parent_id) AS TableName,
                    OBJECT_DEFINITION(t.object_id) AS TriggerDefinition
                FROM 
                    sys.triggers t
                INNER JOIN 
                    sys.tables tab ON t.parent_id = tab.object_id";

                    using (SqlCommand cmd = new SqlCommand(queryTriggers, connection))
                    using (SqlDataReader reader = cmd.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            string triggerName = reader["TriggerName"].ToString();
                            string tableName = reader["TableName"].ToString();
                            string triggerDefinition = reader["TriggerDefinition"].ToString();

                            allTriggers.AppendLine($"-- Trigger: {triggerName} on table {tableName}");
                            allTriggers.AppendLine(triggerDefinition);
                            allTriggers.AppendLine("GO");
                            allTriggers.AppendLine();
                        }
                    }

                    string rutaArchivo = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "Downloads", "triggers_all_tables.sql");
                    File.WriteAllText(rutaArchivo, allTriggers.ToString());

                    Console.WriteLine($"Triggers descargados en: {rutaArchivo}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error al descargar los triggers: {ex.Message}");
            }
        }
















        static List<string> filtros = new List<string>();

        static void GestionarLogsEventosAuditoria()
        {
            while (true)
            {
                Console.WriteLine("\nGestión de Logs de Eventos y Auditoría");
                Console.WriteLine("1. Acceder a logs de eventos y auditoría");
                Console.WriteLine("2. Agregar filtros");
                Console.WriteLine("3. Generar informe PDF con información filtrada");
                Console.WriteLine("4. Volver al menú principal");
                Console.Write("Seleccione una opción: ");

                if (int.TryParse(Console.ReadLine(), out int opcion))
                {
                    switch (opcion)
                    {
                        case 1:
                            AccederLogs();
                            break;
                        case 2:
                            AgregarFiltros();
                            break;
                        case 3:
                            GenerarInformePDFFiltrado();
                            break;
                        case 4:
                            return;
                        default:
                            Console.WriteLine("Opción no válida.");
                            break;
                    }
                }
                else
                {
                    Console.WriteLine("Por favor, ingrese un número válido.");
                }
            }
        }

        static void AccederLogs()
        {
            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();
                    string query = "SELECT * FROM auditoria";

                    if (filtros.Count > 0)
                    {
                        query += " WHERE " + string.Join(" AND ", filtros);
                    }

                    using (SqlCommand command = new SqlCommand(query, connection))
                    using (SqlDataReader reader = command.ExecuteReader())
                    {
                        bool hasRows = false;
                        while (reader.Read())
                        {
                            hasRows = true;
                            Console.WriteLine($"ID: {reader["id"]}, Tabla: {reader["nombre_tabla"]}, Operación: {reader["operacion"]}, Usuario: {reader["usuario_actual"]}, Fecha: {reader["fecha_hora"]}, Detalle Anterior: {reader["detalle_anterior"]}, Detalle Nuevo: {reader["detalle_nuevo"]}");
                        }

                        if (!hasRows)
                        {
                            Console.WriteLine("No se encontraron registros con los filtros aplicados.");
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error al acceder a los logs: {ex.Message}");
            }
        }

        static void AgregarFiltros()
        {
            Console.WriteLine("Ingrese el filtro en formato SQL (ejemplo: operacion = 'INSERT'):");
            string filtro = Console.ReadLine();

            if (ValidarFiltro(filtro))
            {
                filtros.Add(filtro);
                Console.WriteLine("Filtro agregado correctamente.");
            }
            else
            {
                Console.WriteLine("Filtro no válido. Por favor, ingrese un filtro en formato SQL correcto.");
            }
        }

        static bool ValidarFiltro(string filtro)
        {
            string[] validColumns = { "id", "nombre_tabla", "operacion", "usuario_actual", "fecha_hora", "detalle_anterior", "detalle_nuevo" };
            string[] filtroParts = filtro.Split(new[] { '=' }, StringSplitOptions.RemoveEmptyEntries);

            if (filtroParts.Length == 2 && validColumns.Contains(filtroParts[0].Trim()))
            {
                return true;
            }

            return false;
        }

        static void GenerarInformePDFFiltrado()
        {
            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();
                    string query = "SELECT * FROM auditoria";
                    if (filtros.Count > 0)
                    {
                        query += " WHERE " + string.Join(" AND ", filtros);
                    }
                    List<Dictionary<string, string>> datos = new List<Dictionary<string, string>>();
                    using (SqlCommand command = new SqlCommand(query, connection))
                    using (SqlDataReader reader = command.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            datos.Add(new Dictionary<string, string>
                    {
                        {"ID", reader["id"].ToString()},
                        {"Tabla", reader["nombre_tabla"].ToString()},
                        {"Operación", reader["operacion"].ToString()},
                        {"Usuario", reader["usuario_actual"].ToString()},
                        {"Fecha", reader["fecha_hora"].ToString()},
                        {"Detalle Anterior", reader["detalle_anterior"].ToString()},
                        {"Detalle Nuevo", reader["detalle_nuevo"].ToString()}
                    });
                        }
                    }
                    string rutaPDF = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "InformeLogsFiltrados.pdf");
                    using (PdfWriter writer = new PdfWriter(rutaPDF))
                    using (PdfDocument pdf = new PdfDocument(writer))
                    using (Document document = new Document(pdf, iText.Kernel.Geom.PageSize.A4.Rotate()))
                    {
                        document.SetMargins(20, 20, 20, 20);

                        document.Add(new Paragraph("Informe de Logs de Eventos y Auditoría (Filtrado)").SetFontSize(14).SetBold());
                        document.Add(new Paragraph($"Fecha de generación: {DateTime.Now}").SetFontSize(10));
                        document.Add(new Paragraph($"Filtros aplicados: {string.Join(", ", filtros)}").SetFontSize(10));
                        document.Add(new Paragraph("\n"));

                        Table table = new Table(UnitValue.CreatePercentArray(new float[] { 5, 10, 10, 10, 15, 25, 25 })).UseAllAvailableWidth();

                        Cell headerCell = new Cell().SetBackgroundColor(ColorConstants.LIGHT_GRAY).SetTextAlignment(TextAlignment.CENTER);
                        string[] headers = { "ID", "Tabla", "Operación", "Usuario", "Fecha", "Detalle Anterior", "Detalle Nuevo" };
                        foreach (var header in headers)
                        {
                            table.AddHeaderCell(headerCell.Clone(false).Add(new Paragraph(header).SetFontSize(9).SetBold()));
                        }

                        foreach (var dato in datos)
                        {
                            foreach (var key in dato.Keys)
                            {
                                table.AddCell(new Cell().SetTextAlignment(TextAlignment.CENTER).Add(new Paragraph(dato[key]).SetFontSize(8)));
                            }
                        }

                        document.Add(table);
                    }
                    Console.WriteLine($"Informe PDF generado: {rutaPDF}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error al generar el informe PDF: {ex.Message}");
            }
        }















        static void GenerarTriggersAuditoria()
        {
            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();

                    // Obtener todas las tablas excepto la tabla de auditoría
                    string tableQuery = @"
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE' 
            AND TABLE_NAME != 'auditoria'";

                    List<string> tables = new List<string>();

                    using (SqlCommand command = new SqlCommand(tableQuery, connection))
                    using (SqlDataReader reader = command.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            tables.Add(reader.GetString(0));
                        }
                    }

                    foreach (string tableName in tables)
                    {
                        GenerarTriggerParaTabla(connection, tableName);
                    }

                    Console.WriteLine("Triggers de auditoría generados correctamente para todas las tablas.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error al generar triggers de auditoría: {ex.Message}");
            }
        }

        static void GenerarTriggerParaTabla(SqlConnection connection, string tableName)
        {
            string triggerInsert = $@"
CREATE TRIGGER [dbo].[{tableName}_AFTER_INSERT] ON [dbo].[{tableName}]
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO [dbo].[auditoria] ([nombre_tabla], [operacion], [usuario_actual], [detalle_nuevo])
    SELECT '{tableName}', 'INSERT', SYSTEM_USER, 
    (SELECT * FROM inserted FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
END;";

            string triggerUpdate = $@"
CREATE TRIGGER [dbo].[{tableName}_AFTER_UPDATE] ON [dbo].[{tableName}]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO [dbo].[auditoria] ([nombre_tabla], [operacion], [usuario_actual], [detalle_anterior], [detalle_nuevo])
    SELECT '{tableName}', 'UPDATE', SYSTEM_USER, 
    (SELECT * FROM deleted FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
    (SELECT * FROM inserted FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
END;";

            string triggerDelete = $@"
CREATE TRIGGER [dbo].[{tableName}_AFTER_DELETE] ON [dbo].[{tableName}]
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO [dbo].[auditoria] ([nombre_tabla], [operacion], [usuario_actual], [detalle_anterior])
    SELECT '{tableName}', 'DELETE', SYSTEM_USER, 
    (SELECT * FROM deleted FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
END;";

            using (SqlCommand command = new SqlCommand(triggerInsert, connection))
            {
                command.ExecuteNonQuery();
            }

            using (SqlCommand command = new SqlCommand(triggerUpdate, connection))
            {
                command.ExecuteNonQuery();
            }

            using (SqlCommand command = new SqlCommand(triggerDelete, connection))
            {
                command.ExecuteNonQuery();
            }

            Console.WriteLine($"Triggers generados para la tabla {tableName}");
        }













        static void CrearTablaAuditoria()
        {
            Console.Write("Ingrese el nombre de la tabla de auditoría: ");
            string nombreTabla = Console.ReadLine();

            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();
                string query = $@"
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = '{nombreTabla}')
            BEGIN
                CREATE TABLE {nombreTabla} (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    nombre_tabla VARCHAR(255),
                    operacion VARCHAR(10),
                    usuario_actual VARCHAR(255),
                    fecha_hora DATETIME2 DEFAULT GETDATE(),
                    detalle_anterior NVARCHAR(MAX),
                    detalle_nuevo NVARCHAR(MAX)
                );
                PRINT 'Tabla creada correctamente.';
            END
            ELSE
            BEGIN
                PRINT 'La tabla ya existe.';
            END";

                using (SqlCommand command = new SqlCommand(query, connection))
                {
                    try
                    {
                        command.ExecuteNonQuery();
                        Console.WriteLine($"Operación completada para la tabla '{nombreTabla}'.");
                    }
                    catch (SqlException ex)
                    {
                        Console.WriteLine($"Error al crear la tabla '{nombreTabla}': {ex.Message}");
                    }
                }
            }
        }












        static void CrearLoginYUsuario()
        {
            Console.Write("Ingrese el nombre del nuevo login: ");
            string nombreLogin = Console.ReadLine();

            Console.Write("Ingrese la contraseña del nuevo login: ");
            string contraseñaLogin = Console.ReadLine();

            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();

                // Verificar si el login ya existe
                string verificarLoginQuery = $"SELECT name FROM sys.server_principals WHERE type_desc IN ('SQL_LOGIN', 'WINDOWS_LOGIN') AND name = @nombreLogin";
                using (SqlCommand verificarLoginCmd = new SqlCommand(verificarLoginQuery, connection))
                {
                    verificarLoginCmd.Parameters.AddWithValue("@nombreLogin", nombreLogin);
                    object resultado = verificarLoginCmd.ExecuteScalar();
                    if (resultado != null)
                    {
                        Console.WriteLine($"El login '{nombreLogin}' ya existe en el servidor.");
                        return;
                    }
                }

                // Crear el login
                string createLoginQuery = $"CREATE LOGIN [{nombreLogin}] WITH PASSWORD = '{contraseñaLogin}'";
                using (SqlCommand createLoginCommand = new SqlCommand(createLoginQuery, connection))
                {
                    try
                    {
                        createLoginCommand.ExecuteNonQuery();
                        Console.WriteLine($"Login '{nombreLogin}' creado correctamente.");
                        Console.WriteLine("");
                    }
                    catch (SqlException ex)
                    {
                        Console.WriteLine($"Error al crear el login: {ex.Message}");
                        return;
                    }
                }

                // Crear el usuario asociado al login en una base de datos específica
                Console.Write("Ingrese el nombre de la base de datos para crear el usuario: ");
                string nombreBaseDeDatos = Console.ReadLine();

                // Verificar si la base de datos existe
                string verificarBaseDeDatosQuery = $"SELECT name FROM sys.databases WHERE name = @nombreBaseDeDatos";
                using (SqlCommand verificarBaseDeDatosCmd = new SqlCommand(verificarBaseDeDatosQuery, connection))
                {
                    verificarBaseDeDatosCmd.Parameters.AddWithValue("@nombreBaseDeDatos", nombreBaseDeDatos);
                    object resultado = verificarBaseDeDatosCmd.ExecuteScalar();
                    if (resultado == null)
                    {
                        Console.WriteLine($"La base de datos '{nombreBaseDeDatos}' no existe en el servidor.");
                        return;
                    }
                }

                // Crear el usuario
                string createUsuarioQuery = $"USE {nombreBaseDeDatos}; CREATE USER [{nombreLogin}] FOR LOGIN [{nombreLogin}]";
                using (SqlCommand createUsuarioCommand = new SqlCommand(createUsuarioQuery, connection))
                {
                    try
                    {
                        createUsuarioCommand.ExecuteNonQuery();
                        Console.WriteLine($"Usuario '{nombreLogin}' creado correctamente en la base de datos '{nombreBaseDeDatos}'.");
                        Console.WriteLine(" ");
                    }
                    catch (SqlException ex)
                    {
                        Console.WriteLine($"Error al crear el usuario: {ex.Message}");
                        return;
                    }
                }
            }
        }



        static void ModificarUsuario()
        {
            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();

                // Obtener la lista de usuarios disponibles en la base de datos
                Dictionary<int, string> usuarios = new Dictionary<int, string>();
                string obtenerUsuariosQuery = "SELECT principal_id, name FROM sys.database_principals WHERE type_desc = 'SQL_USER'";
                using (SqlCommand obtenerUsuariosCmd = new SqlCommand(obtenerUsuariosQuery, connection))
                {
                    using (SqlDataReader reader = obtenerUsuariosCmd.ExecuteReader())
                    {
                        int index = 1;
                        while (reader.Read())
                        {
                            int principalId = reader.GetInt32(0);
                            string nombreUser = reader.GetString(1);
                            usuarios.Add(index, nombreUser);
                            Console.WriteLine($"{index}. {nombreUser}");
                            index++;
                        }
                    }
                }

                // Solicitar al usuario que seleccione el número del usuario a modificar
                Console.Write("\nIngrese el número del usuario a modificar: ");
                if (!int.TryParse(Console.ReadLine(), out int seleccion))
                {
                    Console.WriteLine("Entrada no válida. Debe ingresar un número.");
                    return;
                }

                // Verificar si el número de usuario seleccionado existe
                if (!usuarios.ContainsKey(seleccion))
                {
                    Console.WriteLine("Número de usuario no válido.");
                    return;
                }

                string nombreUsuario = usuarios[seleccion];

                // Solicitar al usuario que ingrese el nuevo nombre para el usuario seleccionado
                Console.Write("Ingrese el nuevo nombre para el usuario: ");
                string nuevoNombreUsuario = Console.ReadLine();

                // Modificar el nombre del usuario
                string query = $"ALTER USER [{nombreUsuario}] WITH NAME = [{nuevoNombreUsuario}]";
                using (SqlCommand command = new SqlCommand(query, connection))
                {
                    try
                    {
                        command.ExecuteNonQuery();
                        Console.WriteLine($"Usuario '{nombreUsuario}' modificado correctamente. Nuevo nombre: '{nuevoNombreUsuario}'");
                    }
                    catch (SqlException ex)
                    {
                        Console.WriteLine($"Error al modificar el usuario: {ex.Message}");
                    }
                }
            }
        }

        static void EliminarUsuario()
        {
            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();

                // Obtener la lista de usuarios disponibles en la base de datos
                Dictionary<int, string> usuarios = new Dictionary<int, string>();
                string obtenerUsuariosQuery = "SELECT principal_id, name FROM sys.database_principals WHERE type_desc = 'SQL_USER'";
                using (SqlCommand obtenerUsuariosCmd = new SqlCommand(obtenerUsuariosQuery, connection))
                {
                    using (SqlDataReader reader = obtenerUsuariosCmd.ExecuteReader())
                    {
                        int index = 1;
                        while (reader.Read())
                        {
                            int principalId = reader.GetInt32(0);
                            string nombreUser = reader.GetString(1);
                            usuarios.Add(index, nombreUser);
                            Console.WriteLine($"{index}. {nombreUser}");
                            index++;
                        }
                    }
                }

                // Solicitar al usuario que seleccione el número del usuario a eliminar
                Console.Write("\nIngrese el número del usuario a eliminar: ");
                if (!int.TryParse(Console.ReadLine(), out int seleccion))
                {
                    Console.WriteLine("Entrada no válida. Debe ingresar un número.");
                    return;
                }

                // Verificar si el número de usuario seleccionado existe
                if (!usuarios.ContainsKey(seleccion))
                {
                    Console.WriteLine("Número de usuario no válido.");
                    return;
                }

                string nombreUsuario = usuarios[seleccion];

                // Eliminar el usuario
                string eliminarUsuarioQuery = $"DROP USER [{nombreUsuario}]";
                using (SqlCommand eliminarUsuarioCmd = new SqlCommand(eliminarUsuarioQuery, connection))
                {
                    try
                    {
                        eliminarUsuarioCmd.ExecuteNonQuery();
                        Console.WriteLine($"Usuario '{nombreUsuario}' eliminado correctamente.");
                    }
                    catch (SqlException ex)
                    {
                        Console.WriteLine($"Error al eliminar el usuario: {ex.Message}");
                    }
                }
            }
        }

        static void CrearRol()
        {
            Console.Write("Ingrese el nombre del nuevo rol: ");
            string nombreRol = Console.ReadLine();

            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();

                string query = $"CREATE ROLE [{nombreRol}]";
                SqlCommand command = new SqlCommand(query, connection);

                try
                {
                    command.ExecuteNonQuery();
                    Console.WriteLine($"Rol '{nombreRol}' creado correctamente.");
                    Console.WriteLine(" ");

                }
                catch (SqlException ex)
                {
                    Console.WriteLine($"Error al crear el rol: {ex.Message}");
                }
            }
        }

        static void AsignarRolUsuario()
        {
            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();

                // Obtener la lista de usuarios disponibles en la base de datos
                Dictionary<int, string> usuarios = new Dictionary<int, string>();
                string obtenerUsuariosQuery = "SELECT principal_id, name FROM sys.database_principals WHERE type_desc = 'SQL_USER'";
                using (SqlCommand obtenerUsuariosCmd = new SqlCommand(obtenerUsuariosQuery, connection))
                {
                    using (SqlDataReader reader = obtenerUsuariosCmd.ExecuteReader())
                    {
                        int index = 1;
                        Console.WriteLine("Usuarios disponibles:");
                        while (reader.Read())
                        {
                            int principalId = reader.GetInt32(0);
                            string nombreUser = reader.GetString(1);
                            usuarios.Add(index, nombreUser);
                            Console.WriteLine($"{index}. {nombreUser}");
                            index++;
                        }
                    }
                }

                // Solicitar al usuario que seleccione el número del usuario
                Console.Write("\nIngrese el número del usuario: ");
                if (!int.TryParse(Console.ReadLine(), out int seleccionUsuario))
                {
                    Console.WriteLine("Entrada no válida. Debe ingresar un número.");
                    return;
                }

                // Verificar si el número de usuario seleccionado existe
                if (!usuarios.ContainsKey(seleccionUsuario))
                {
                    Console.WriteLine("Número de usuario no válido.");
                    return;
                }

                string nombreUsuario = usuarios[seleccionUsuario];

                // Obtener la lista de roles disponibles en la base de datos
                Dictionary<int, string> roles = new Dictionary<int, string>();
                string obtenerRolesQuery = "SELECT name FROM sys.database_principals WHERE type_desc = 'DATABASE_ROLE'";
                using (SqlCommand obtenerRolesCmd = new SqlCommand(obtenerRolesQuery, connection))
                {
                    using (SqlDataReader reader = obtenerRolesCmd.ExecuteReader())
                    {
                        int index = 1;
                        Console.WriteLine("\nRoles disponibles:");
                        while (reader.Read())
                        {
                            string nameRol = reader.GetString(0);
                            roles.Add(index, nameRol);
                            Console.WriteLine($"{index}. {nameRol}");
                            index++;
                        }
                    }
                }

                // Solicitar al usuario que seleccione el número del rol
                Console.Write("\nIngrese el número del rol: ");
                if (!int.TryParse(Console.ReadLine(), out int seleccionRol))
                {
                    Console.WriteLine("Entrada no válida. Debe ingresar un número.");
                    return;
                }

                // Verificar si el número de rol seleccionado existe
                if (!roles.ContainsKey(seleccionRol))
                {
                    Console.WriteLine("Número de rol no válido.");
                    return;
                }

                string nombreRol = roles[seleccionRol];

                // Asignar el rol al usuario
                string query = $"ALTER ROLE [{nombreRol}] ADD MEMBER [{nombreUsuario}]";
                using (SqlCommand command = new SqlCommand(query, connection))
                {
                    try
                    {
                        command.ExecuteNonQuery();
                        Console.WriteLine($"Rol '{nombreRol}' asignado al usuario '{nombreUsuario}' correctamente.");
                    }
                    catch (SqlException ex)
                    {
                        Console.WriteLine($"Error al asignar el rol al usuario: {ex.Message}");
                    }
                }
            }
        }


        static void ConsultarRoles()
        {
            Console.WriteLine("Roles en la base de datos:");
            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();

                string query = "SELECT name FROM sys.database_principals WHERE type_desc = 'DATABASE_ROLE'";
                SqlCommand command = new SqlCommand(query, connection);

                SqlDataReader reader = command.ExecuteReader();
                Console.WriteLine("");
                while (reader.Read())
                {

                    Console.WriteLine(reader["name"]);


                }
                reader.Close();
            }
        }

        static void ConsultarUsuarios()
        {
            Console.WriteLine("Usuarios en la base de datos:");
            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();

                string query = "SELECT name FROM sys.database_principals WHERE type_desc = 'SQL_USER'";
                SqlCommand command = new SqlCommand(query, connection);

                SqlDataReader reader = command.ExecuteReader();
                Console.WriteLine("");
                while (reader.Read())
                {
                    Console.WriteLine(reader["name"]);

                }
                reader.Close();
            }
        }


        static void RealizarRespaldo()
        {
            try
            {
                Console.Write("Ingrese el nombre de la base de datos a respaldar: ");
                string databaseName = Console.ReadLine();
                Console.Write("Ingrese el nombre del archivo de respaldo (.bak): ");
                string fileName = Console.ReadLine();
                string backupFolderPath = @"C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\Backup";
                string backupFileName = Path.Combine(backupFolderPath, fileName);

                if (File.Exists(backupFileName))
                {
                    Console.WriteLine("El archivo de respaldo ya existe en la ubicación especificada.");
                    return;
                }

                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();

                    // Comando SQL para realizar el respaldo
                    string query = $"BACKUP DATABASE [{databaseName}] TO DISK = '{backupFileName}'";
                    SqlCommand command = new SqlCommand(query, connection);
                    command.ExecuteNonQuery();

                    Console.WriteLine($"Respaldo de la base de datos '{databaseName}' creado correctamente en '{backupFileName}'.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error al realizar el respaldo: {ex.Message}");
            }
        }

        static void RestaurarBaseDeDatos()
        {
            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();

                try
                {
                    // Mostrar los archivos de respaldo disponibles
                    string backupPath = @"C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\Backup";
                    string[] backupFiles = Directory.GetFiles(backupPath, "*.bak");

                    if (backupFiles.Length > 0)
                    {
                        Console.WriteLine("Seleccione el archivo de respaldo a restaurar:");
                        for (int i = 0; i < backupFiles.Length; i++)
                        {
                            Console.WriteLine($"{i + 1}. {Path.GetFileName(backupFiles[i])}");
                        }

                        Console.Write("Ingrese el número correspondiente: ");
                        int selectedIndex;
                        if (int.TryParse(Console.ReadLine(), out selectedIndex) && selectedIndex >= 1 && selectedIndex <= backupFiles.Length)
                        {
                            string backupFilePath = backupFiles[selectedIndex - 1];
                            string backupFileName = Path.GetFileName(backupFilePath);

                            // Restaurar la base de datos desde el archivo de respaldo seleccionado
                            string databaseName = Path.GetFileNameWithoutExtension(backupFileName).Split('_')[0];
                            string newDataPath = @"C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\";
                            string newLogPath = @"C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\";

                            string query = $"RESTORE DATABASE [{databaseName}] FROM DISK = '{backupFilePath}' " +
                                           $"WITH MOVE 'TalentoHumano' TO '{newDataPath}{databaseName}.mdf', " +
                                           $"MOVE 'TalentoHumano_log' TO '{newLogPath}{databaseName}_log.ldf', " +
                                           $"REPLACE";

                            SqlCommand command = new SqlCommand(query, connection);
                            command.ExecuteNonQuery();

                            Console.WriteLine($"Se restauró la base de datos '{databaseName}' desde el archivo '{backupFileName}'");

                            // Obtener información adicional de la base de datos restaurada
                        }
                        else
                        {
                            Console.WriteLine("Selección inválida.");
                        }
                    }
                    else
                    {
                        Console.WriteLine("No hay archivos de respaldo disponibles.");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error al restaurar la base de datos: {ex.Message}");
                }
            }
        }


        static void ListarEntidadesBaseDatos()
        {
            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();

                    // Consulta SQL para obtener la lista de entidades de la base de datos
                    string query = "SELECT name FROM sys.objects WHERE type IN ('U', 'V', 'P', 'FN', 'TF', 'IF') ORDER BY name";

                    using (SqlCommand command = new SqlCommand(query, connection))
                    {
                        using (SqlDataReader reader = command.ExecuteReader())
                        {
                            Console.WriteLine("Lista de entidades en la base de datos:");

                            // Iterar sobre los resultados y mostrar el nombre de cada entidad
                            while (reader.Read())
                            {
                                string entityName = reader.GetString(0);
                                Console.WriteLine("- " + entityName);
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error al listar las entidades: " + ex.Message);
            }
        }

        static void ListarAtributosEntidad()
        {
            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();

                    // Consulta SQL para obtener la lista de entidades de la base de datos
                    string query = "SELECT object_id, name FROM sys.objects WHERE type IN ('U', 'V', 'P', 'FN', 'TF', 'IF') ORDER BY name";

                    Dictionary<int, string> entityDictionary = new Dictionary<int, string>();

                    using (SqlCommand command = new SqlCommand(query, connection))
                    {
                        using (SqlDataReader reader = command.ExecuteReader())
                        {
                            Console.WriteLine("Lista de entidades en la base de datos:");

                            // Iterar sobre los resultados y mostrar el nombre de cada entidad con un ID asignado
                            int entityId = 1;
                            while (reader.Read())
                            {
                                string entityName = reader.GetString(1);
                                Console.WriteLine($"{entityId}. {entityName}");
                                entityDictionary.Add(entityId, entityName);
                                entityId++;
                            }
                        }
                    }

                    Console.Write("Seleccione el número de la entidad para ver sus atributos (o 0 para salir): ");
                    if (int.TryParse(Console.ReadLine(), out int selectedEntityId) && entityDictionary.ContainsKey(selectedEntityId))
                    {
                        string selectedEntity = entityDictionary[selectedEntityId];
                        MostrarAtributosEntidad(connection, selectedEntity);
                    }
                    else
                    {
                        Console.WriteLine("Selección no válida o no seleccionada. Saliendo del programa.");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error al listar los atributos de las entidades: " + ex.Message);
            }
        }

        static void MostrarAtributosEntidad(SqlConnection connection, string entityName)
        {
            try
            {
                // Consulta SQL para obtener los atributos de la entidad seleccionada
                string query = "SELECT name FROM sys.columns WHERE object_id = OBJECT_ID(@entityName)";

                using (SqlCommand command = new SqlCommand(query, connection))
                {
                    command.Parameters.AddWithValue("@entityName", entityName);

                    using (SqlDataReader reader = command.ExecuteReader())
                    {
                        Console.WriteLine("Atributos de la entidad " + entityName + ":");

                        // Iterar sobre los resultados y mostrar el nombre de cada atributo
                        while (reader.Read())
                        {
                            string attributeName = reader.GetString(0);
                            Console.WriteLine("- " + attributeName);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error al listar los atributos de la entidad " + entityName + ": " + ex.Message);
            }
        }
        static void AgregarEntidadConAtributos()
        {
            Console.Write("Ingrese el nombre de la entidad: ");
            string nombreEntidad = Console.ReadLine();

            Console.WriteLine("Ingrese los atributos de la entidad (separados por coma): ");
            string atributosInput = Console.ReadLine();
            string[] atributos = atributosInput.Split(',');

            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();

                    // Verificar si la entidad ya existe en la base de datos
                    string verificarEntidadQuery = $"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = @nombreEntidad";
                    using (SqlCommand verificarEntidadCmd = new SqlCommand(verificarEntidadQuery, connection))
                    {
                        verificarEntidadCmd.Parameters.AddWithValue("@nombreEntidad", nombreEntidad);
                        int count = (int)verificarEntidadCmd.ExecuteScalar();
                        if (count > 0)
                        {
                            Console.WriteLine($"La entidad '{nombreEntidad}' ya existe en la base de datos.");
                            return;
                        }
                    }

                    // Consulta SQL para agregar una nueva tabla
                    string createTableQuery = $"CREATE TABLE {nombreEntidad} (ID INT PRIMARY KEY";
                    foreach (var atributo in atributos)
                    {
                        createTableQuery += $", {atributo} NVARCHAR(50)";
                    }
                    createTableQuery += ")";

                    using (SqlCommand command = new SqlCommand(createTableQuery, connection))
                    {
                        command.ExecuteNonQuery();
                        Console.WriteLine($"Se ha creado la nueva entidad '{nombreEntidad}' correctamente.");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error al agregar la nueva entidad con atributos: " + ex.Message);
            }
        }

        static void GenerarInformePDF()
        {
            string rutaPDF = "C:/Users/Ivani/Desktop/Informe.pdf"; // Ruta para el archivo PDF
            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();
                    // Consulta SQL para obtener la lista de tablas en la base de datos
                    string query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_CATALOG = @Database ORDER BY TABLE_NAME";

                    List<string> entities = new List<string>();

                    using (SqlCommand command = new SqlCommand(query, connection))
                    {
                        command.Parameters.AddWithValue("@Database", connection.Database);

                        using (SqlDataReader reader = command.ExecuteReader())
                        {
                            Console.WriteLine("Entidades disponibles:");
                            int entityId = 1;
                            while (reader.Read())
                            {
                                string tableName = reader.GetString(0);
                                entities.Add(tableName);
                                Console.WriteLine($"{entityId}. {tableName}");
                                entityId++;
                            }
                        }
                    }

                    // Permitir al usuario la selección de la entidad
                    Console.Write("Seleccione el número de la entidad que desea mostrar en el informe: ");
                    if (int.TryParse(Console.ReadLine(), out int selectedEntityId) && selectedEntityId > 0 && selectedEntityId <= entities.Count)
                    {
                        string selectedEntity = entities[selectedEntityId - 1];

                        // Consulta SQL para obtener los atributos de la entidad seleccionada
                        string attributeQuery = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_CATALOG = @Database AND TABLE_NAME = @TableName";

                        List<string> attributes = new List<string>();

                        using (SqlCommand attributeCommand = new SqlCommand(attributeQuery, connection))
                        {
                            attributeCommand.Parameters.AddWithValue("@Database", connection.Database);
                            attributeCommand.Parameters.AddWithValue("@TableName", selectedEntity);

                            using (SqlDataReader attributeReader = attributeCommand.ExecuteReader())
                            {
                                // Mostrar los atributos disponibles para seleccionar
                                Console.WriteLine($"Atributos disponibles para la entidad '{selectedEntity}':");
                                while (attributeReader.Read())
                                {
                                    string attributeName = attributeReader.GetString(0);
                                    attributes.Add(attributeName);
                                    Console.WriteLine(attributeName);
                                }
                            }
                        }
                        Console.WriteLine("Ingrese los nombres de los atributos que desea mostrar (separados por coma):");
                        string selectedAttributesInput = Console.ReadLine();
                        string[] selectedAttributes = selectedAttributesInput.Split(',');

                        // Verificar que los atributos seleccionados son válidos
                        foreach (var attr in selectedAttributes)
                        {
                            if (!attributes.Contains(attr.Trim()))
                            {
                                Console.WriteLine($"El atributo '{attr.Trim()}' no es válido para la entidad '{selectedEntity}'.");
                                return;
                            }
                        }

                        // Crear la consulta SQL para obtener los datos de los atributos seleccionados
                        string columns = string.Join(", ", selectedAttributes);
                        string dataQuery = $"SELECT {columns} FROM {selectedEntity}";

                        List<Dictionary<string, object>> data = new List<Dictionary<string, object>>();

                        using (SqlCommand dataCommand = new SqlCommand(dataQuery, connection))
                        {
                            using (SqlDataReader dataReader = dataCommand.ExecuteReader())
                            {
                                // Leer los datos y almacenarlos en una lista de diccionarios
                                while (dataReader.Read())
                                {
                                    Dictionary<string, object> row = new Dictionary<string, object>();
                                    foreach (var attr in selectedAttributes)
                                    {
                                        row[attr.Trim()] = dataReader[attr.Trim()];
                                    }
                                    data.Add(row);
                                }
                            }
                        }

                        // Mostrar el informe en pantalla
                        Console.WriteLine($"\nInforme de la entidad: {selectedEntity}");
                        foreach (var row in data)
                        {
                            foreach (var kvp in row)
                            {
                                Console.WriteLine($"{kvp.Key}: {kvp.Value}");
                            }
                            Console.WriteLine();
                        }

                        // Preguntar al usuario si desea guardar el informe en PDF
                        Console.WriteLine("¿Desea guardar el informe en PDF? (s/n):");
                        string savePdfResponse = Console.ReadLine();

                        if (savePdfResponse.ToLower() == "s")
                        {
                            // Crear un nuevo documento PDF
                            using (PdfWriter writer = new PdfWriter(rutaPDF))
                            using (PdfDocument pdf = new PdfDocument(writer))
                            using (Document document = new Document(pdf))
                            {
                                document.Add(new Paragraph($"Entidad: {selectedEntity}"));

                                // Agregar los datos de los atributos seleccionados de la entidad al documento PDF
                                foreach (var row in data)
                                {
                                    foreach (var kvp in row)
                                    {
                                        document.Add(new Paragraph($"{kvp.Key}: {kvp.Value}"));
                                    }
                                    document.Add(new Paragraph("\n"));
                                }
                            }

                            Console.WriteLine("Informe PDF generado correctamente.");
                        }
                        else
                        {
                            Console.WriteLine("El informe no se guardó en PDF.");
                        }
                    }
                    else
                    {
                        Console.WriteLine("Selección no válida. Saliendo del programa.");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error al generar el informe: " + ex.Message);
            }
        }
        static void GenerarProcedimientosAlmacenados()
        {
            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();

                SqlCommand command = new SqlCommand("SELECT name FROM sys.objects WHERE type = 'U'", connection);
                SqlDataReader reader = command.ExecuteReader();

                List<string> tableNames = new List<string>();

                while (reader.Read())
                {
                    tableNames.Add(reader["name"].ToString());
                }

                reader.Close();

                foreach (var tableName in tableNames)
                {
                    StringBuilder sb = new StringBuilder();

                    sb.AppendLine($"-- Procedimientos almacenados para la tabla {tableName}");
                    sb.AppendLine();

                    // Procedimiento almacenado para INSERT
                    sb.AppendLine($"CREATE PROCEDURE [dbo].[Insertar{tableName}]");
                    sb.AppendLine("AS");
                    sb.AppendLine("BEGIN");
                    sb.AppendLine($"    INSERT INTO {tableName} (");

                    SqlCommand columnCommand = new SqlCommand($"SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('{tableName}')", connection);
                    SqlDataReader columnReader = columnCommand.ExecuteReader();
                    List<string> columnNames = new List<string>();
                    while (columnReader.Read())
                    {
                        columnNames.Add(columnReader["name"].ToString());
                    }
                    columnReader.Close();

                    sb.AppendLine(string.Join(", ", columnNames.Select(c => $"        {c}")));
                    sb.AppendLine("    )");
                    sb.AppendLine("    VALUES (");
                    sb.AppendLine(string.Join(", ", columnNames.Select(c => $"        @{c}")));
                    sb.AppendLine("    )");
                    sb.AppendLine("END");
                    sb.AppendLine("GO");
                    sb.AppendLine();

                    // Procedimiento almacenado para UPDATE
                    sb.AppendLine($"CREATE PROCEDURE [dbo].[Actualizar{tableName}]");
                    sb.AppendLine("AS");
                    sb.AppendLine("BEGIN");
                    sb.AppendLine($"    UPDATE {tableName}");
                    sb.AppendLine("    SET");

                    foreach (var columnName in columnNames)
                    {
                        sb.AppendLine($"        {columnName} = @{columnName},");
                    }

                    sb.Remove(sb.Length - 3, 1);
                    sb.AppendLine("    WHERE /Condición/");
                    sb.AppendLine("END");
                    sb.AppendLine("GO");
                    sb.AppendLine();

                    // Procedimiento almacenado para DELETE
                    sb.AppendLine($"CREATE PROCEDURE [dbo].[Eliminar{tableName}]");
                    sb.AppendLine("AS");
                    sb.AppendLine("BEGIN");
                    sb.AppendLine($"    DELETE FROM {tableName}");
                    sb.AppendLine("    WHERE /Condición/");
                    sb.AppendLine("END");
                    sb.AppendLine("GO");
                    sb.AppendLine();

                    // Procedimiento almacenado para SELECT
                    sb.AppendLine($"CREATE PROCEDURE [dbo].[Seleccionar{tableName}]");
                    sb.AppendLine("AS");
                    sb.AppendLine("BEGIN");
                    sb.AppendLine($"    SELECT * FROM {tableName}");
                    sb.AppendLine("END");
                    sb.AppendLine("GO");
                    sb.AppendLine();

                    Console.WriteLine(sb.ToString());
                }
            }

        }




    }
}