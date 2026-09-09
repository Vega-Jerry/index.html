
import mysql.connector

from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-sistema-notas-2026"


# ============================================================
# CONFIGURACIÓN DE MYSQL
# ============================================================

def obtener_conexion():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2005Agosto.",
        database="proyecto_web"
    )

    return conn


# ============================================================
# DATOS DE CLIENTES, PROVEEDORES Y FACTURACIÓN
# ============================================================

nombre_sistema = "Sistema de Notas"


clientes_lista = [
    {
        "nombre": "Carlos Méndez",
        "correo": "carlos@gmail.com",
        "telefono": "0991112233",
        "estado": "Activo"
    },
    {
        "nombre": "Ana Torres",
        "correo": "ana@gmail.com",
        "telefono": "0982223344",
        "estado": "Activo"
    },
    {
        "nombre": "Luis Pérez",
        "correo": "luis@gmail.com",
        "telefono": "0973334455",
        "estado": "Inactivo"
    }
]


proveedores_lista = [
    {
        "nombre": "Tech Solutions",
        "correo": "techsolutions@gmail.com",
        "telefono": "0994567890",
        "estado": "Activo"
    },
    {
        "nombre": "Distribuidora Amazon",
        "correo": "distribuidora@gmail.com",
        "telefono": "0985678901",
        "estado": "Activo"
    },
    {
        "nombre": "Servicios Digitales",
        "correo": "servicios@gmail.com",
        "telefono": "0976789012",
        "estado": "Inactivo"
    }
]


facturas_lista = [
    {
        "numero": "001-001-000001",
        "cliente": "Carlos Méndez",
        "fecha": "05/09/2026",
        "total": 120.00,
        "estado": "Pagada"
    },
    {
        "numero": "001-001-000002",
        "cliente": "Ana Torres",
        "fecha": "05/09/2026",
        "total": 250.00,
        "estado": "Pendiente"
    },
    {
        "numero": "001-001-000003",
        "cliente": "Luis Pérez",
        "fecha": "04/09/2026",
        "total": 85.00,
        "estado": "Pagada"
    }
]


# ============================================================
# INICIO
# ============================================================

@app.route("/")
def inicio():

    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema
    )


# ============================================================
# PRODUCTOS - SELECT
# ============================================================

@app.route("/productos")
def productos():

    conn = obtener_conexion()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nombre, descripcion, precio, stock
        FROM productos
        ORDER BY id DESC
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        nombre_sistema=nombre_sistema,
        productos=productos
    )


# ============================================================
# PRODUCTOS - INSERT
# ============================================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos
            (nombre, descripcion, precio, stock)
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.descripcion.data,
            float(form.precio.data),
            form.stock.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        nombre_sistema=nombre_sistema,
        form=form
    )

# ============================================================
# CLIENTES - SELECT
# ============================================================

@app.route("/clientes")
def clientes():

    conn = obtener_conexion()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nombre, correo, telefono, estado
        FROM clientes
        ORDER BY id DESC
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "clientes.html",
        nombre_sistema=nombre_sistema,
        clientes=clientes
    )


# ============================================================
# CLIENTES - INSERT
# ============================================================

@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes
            (nombre, correo, telefono, estado)
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.correo.data,
            form.telefono.data,
            form.estado.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        nombre_sistema=nombre_sistema,
        form=form
    )
# ============================================================
# PROVEEDORES - SELECT
# ============================================================

@app.route("/proveedores")
def proveedores():

    conn = obtener_conexion()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nombre, correo, telefono, estado
        FROM proveedores
        ORDER BY id DESC
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "proveedores.html",
        nombre_sistema=nombre_sistema,
        proveedores=proveedores
    )


# ============================================================
# PROVEEDORES - INSERT
# ============================================================

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores
            (nombre, correo, telefono, estado)
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.correo.data,
            form.telefono.data,
            form.estado.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        nombre_sistema=nombre_sistema,
        form=form
    )
# ============================================================
# FACTURACIÓN - SELECT
# ============================================================

@app.route("/facturacion")
def facturacion():

    conn = obtener_conexion()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, numero, cliente, fecha, total, estado
        FROM facturas
        ORDER BY id DESC
    """)

    facturas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "facturacion.html",
        nombre_sistema=nombre_sistema,
        facturas=facturas
    )


# ============================================================
# FACTURACIÓN - INSERT
# ============================================================

@app.route("/facturacion/nueva", methods=["GET", "POST"])
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facturas
            (numero, cliente, fecha, total, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            form.numero.data,
            form.cliente.data,
            form.fecha.data,
            float(form.total.data),
            form.estado.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        nombre_sistema=nombre_sistema,
        form=form
    )
# ============================================================
# EJECUTAR APLICACIÓN
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)

