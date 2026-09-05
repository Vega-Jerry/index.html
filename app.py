import sqlite3
from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-sistema-notas-2026"


# ============================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================

DATABASE = "data/ferreteria.db"


def obtener_conexion():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_base_datos():

    conn = obtener_conexion()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


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

    productos = conn.execute("""
        SELECT id, nombre, categoria, precio, stock
        FROM productos
        ORDER BY id DESC
    """).fetchall()

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

        conn.execute("""
            INSERT INTO productos
            (nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?)
        """, (
            form.nombre.data,
            form.categoria.data,
            float(form.precio.data),
            form.stock.data
        ))

        conn.commit()
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
# CLIENTES
# ============================================================

@app.route("/clientes")
def clientes():

    return render_template(
        "clientes.html",
        nombre_sistema=nombre_sistema,
        clientes=clientes_lista
    )


@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        nuevo = {
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data,
            "estado": form.estado.data
        }

        clientes_lista.append(nuevo)

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
# PROVEEDORES
# ============================================================

@app.route("/proveedores")
def proveedores():

    return render_template(
        "proveedores.html",
        nombre_sistema=nombre_sistema,
        proveedores=proveedores_lista
    )


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        nuevo = {
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data,
            "estado": form.estado.data
        }

        proveedores_lista.append(nuevo)

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
# FACTURACIÓN
# ============================================================

@app.route("/facturacion")
def facturacion():

    return render_template(
        "facturacion.html",
        nombre_sistema=nombre_sistema,
        facturas=facturas_lista
    )


@app.route("/facturacion/nueva", methods=["GET", "POST"])
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        nueva = {
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "fecha": form.fecha.data.strftime("%d/%m/%Y"),
            "total": float(form.total.data),
            "estado": form.estado.data
        }

        facturas_lista.append(nueva)

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
# INICIALIZAR BASE DE DATOS
# ============================================================

inicializar_base_datos()


# ============================================================
# EJECUTAR APLICACIÓN
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)