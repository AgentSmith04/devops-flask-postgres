from flask import Flask
import psycopg2

app = Flask(__name__)

VERSION = "2.0.0"


def obtener_conexion():
    return psycopg2.connect(
        host="db",
        database="empresa",
        user="admin",
        password="admin123"
    )


@app.route("/")
def inicio():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT version();")
        version_postgres = cursor.fetchone()

        cursor.execute("SELECT id, nombre FROM clientes ORDER BY id;")
        clientes = cursor.fetchall()

        cursor.close()
        conexion.close()

        lista_clientes = ""

        for cliente in clientes:
            lista_clientes += f"<li>{cliente[0]} - {cliente[1]}</li>"

        return f"""
        <h1>Aplicación Flask</h1>
        <h2>Versión {VERSION}</h2>
        <p>Conexión exitosa a PostgreSQL</p>
        <p>{version_postgres}</p>

        <h2>Clientes registrados</h2>
        <ul>
            {lista_clientes}
        </ul>
        """

    except Exception as e:
        return f"""
        <h1>Error</h1>
        <p>{e}</p>
        """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)