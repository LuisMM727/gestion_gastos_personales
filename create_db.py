import mysql.connector

try:
    conn = mysql.connector.connect(
        user='root',
        host='localhost'
    )
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS gestion_gastos_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
    conn.commit()
    print('✓ Base de datos gestion_gastos_db creada exitosamente')
    cursor.close()
    conn.close()
except mysql.connector.Error as err:
    print(f'Error: {err}')
except Exception as e:
    print(f'Error de conexión: {e}')
    print('Asegúrate de que MySQL está instalado y corriendo en localhost:3306')
