import os

import psycopg2
from psycopg2.extras import RealDictCursor

from flask import Flask, render_template, redirect, url_for, flash

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


# =========================================================
# CONFIGURACIÓN
# =========================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-sistema-notas-2026"


# =========================================================
# FLASK-LOGIN
# =========================================================

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"


# =========================================================
# CONEXIÓN A POSTGRESQL
# =========================================================

def obtener_conexion():

    # Para Render
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg2.connect(
            database_url,
            sslmode="require"
        )

    # Para trabajar localmente
    return psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="2005Agosto.",
        database="proyecto_web"
    )


# =========================================================
# USUARIO
# =========================================================

class Usuario(UserMixin):

    def __init__(self, id, usuario):
        self.id = id
        self.usuario = usuario


@login_manager.user_loader
def cargar_usuario(user_id):

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT id, usuario
        FROM usuarios
        WHERE id = %s
        """,
        (user_id,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario:

        return Usuario(
            usuario["id"],
            usuario["usuario"]
        )

    return None


# =========================================================
# INICIO
# =========================================================

@app.route("/")
@login_required
def inicio():

    return render_template(
        "index.html",
        nombre_sistema="Sistema de Notas"
    )


# =========================================================
# REGISTRO
# =========================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    from forms.usuario_form import UsuarioForm

    form = UsuarioForm()

    if form.validate_on_submit():

        usuario = form.usuario.data
        password = form.password.data

        password_hash = generate_password_hash(password)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO usuarios
                (usuario, password)
                VALUES (%s, %s)
                """,
                (
                    usuario,
                    password_hash
                )
            )

            conexion.commit()

            flash(
                "Usuario registrado correctamente.",
                "success"
            )

            return redirect(
                url_for("login")
            )

        except psycopg2.errors.UniqueViolation:

            conexion.rollback()

            flash(
                "El usuario ya existe.",
                "danger"
            )

        finally:

            cursor.close()
            conexion.close()

    return render_template(
        "registro.html",
        form=form
    )


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    from forms.login_form import LoginForm

    form = LoginForm()

    if form.validate_on_submit():

        usuario_ingresado = form.usuario.data
        password_ingresada = form.password.data

        conexion = obtener_conexion()

        cursor = conexion.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
            """,
            (usuario_ingresado,)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario and check_password_hash(
            usuario["password"],
            password_ingresada
        ):

            usuario_obj = Usuario(
                usuario["id"],
                usuario["usuario"]
            )

            login_user(usuario_obj)

            flash(
                "Inicio de sesión exitoso.",
                "success"
            )

            return redirect(
                url_for("inicio")
            )

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "info"
    )

    return redirect(
        url_for("login")
    )


# =========================================================
# PRODUCTOS - LISTAR
# =========================================================

@app.route("/productos")
@login_required
def productos():

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT
            id,
            nombre,
            descripcion,
            precio,
            stock
        FROM productos
        ORDER BY id DESC
        """
    )

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# =========================================================
# PRODUCTOS - NUEVO
# =========================================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO productos
            (
                nombre,
                descripcion,
                precio,
                stock
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.precio.data,
                form.stock.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("productos")
        )

    return render_template(
        "formulario_producto.html",
        form=form,
        titulo="Nuevo producto"
    )


# =========================================================
# PRODUCTOS - EDITAR
# =========================================================

@app.route(
    "/productos/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar_producto(id):

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT
            id,
            nombre,
            descripcion,
            precio,
            stock
        FROM productos
        WHERE id = %s
        """,
        (id,)
    )

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not producto:

        flash(
            "Producto no encontrado.",
            "danger"
        )

        return redirect(
            url_for("productos")
        )

    form = ProductoForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE productos
            SET
                nombre = %s,
                descripcion = %s,
                precio = %s,
                stock = %s
            WHERE id = %s
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.precio.data,
                form.stock.data,
                id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Producto actualizado correctamente.",
            "success"
        )

        return redirect(
            url_for("productos")
        )

    elif not form.is_submitted():

        form.nombre.data = producto["nombre"]
        form.descripcion.data = producto["descripcion"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]

    return render_template(
        "formulario_producto.html",
        form=form,
        titulo="Editar producto"
    )


# =========================================================
# PRODUCTOS - ELIMINAR
# =========================================================

@app.route(
    "/productos/eliminar/<int:id>",
    methods=["POST"]
)
@login_required
def eliminar_producto(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM productos
            WHERE id = %s
            """,
            (id,)
        )

        conexion.commit()

        flash(
            "Producto eliminado correctamente.",
            "success"
        )

    except psycopg2.errors.ForeignKeyViolation:

        conexion.rollback()

        flash(
            "No se puede eliminar este producto porque está relacionado con una factura.",
            "danger"
        )

    finally:

        cursor.close()
        conexion.close()

    return redirect(
        url_for("productos")
    )


# =========================================================
# CLIENTES - LISTAR
# =========================================================

@app.route("/clientes")
@login_required
def clientes():

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT
            id,
            nombre,
            correo,
            telefono,
            estado
        FROM clientes
        ORDER BY id DESC
        """
    )

    clientes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "clientes.html",
        clientes=clientes
    )


# =========================================================
# CLIENTES - NUEVO
# =========================================================

@app.route(
    "/clientes/nuevo",
    methods=["GET", "POST"]
)
@login_required
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO clientes
            (
                nombre,
                correo,
                telefono,
                estado
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.correo.data,
                form.telefono.data,
                form.estado.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("clientes")
        )

    return render_template(
        "formulario_cliente.html",
        form=form,
        titulo="Nuevo cliente"
    )


# =========================================================
# CLIENTES - EDITAR
# =========================================================

@app.route(
    "/clientes/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar_cliente(id):

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT
            id,
            nombre,
            correo,
            telefono,
            estado
        FROM clientes
        WHERE id = %s
        """,
        (id,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not cliente:

        flash(
            "Cliente no encontrado.",
            "danger"
        )

        return redirect(
            url_for("clientes")
        )

    form = ClienteForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE clientes
            SET
                nombre = %s,
                correo = %s,
                telefono = %s,
                estado = %s
            WHERE id = %s
            """,
            (
                form.nombre.data,
                form.correo.data,
                form.telefono.data,
                form.estado.data,
                id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Cliente actualizado correctamente.",
            "success"
        )

        return redirect(
            url_for("clientes")
        )

    elif not form.is_submitted():

        form.nombre.data = cliente["nombre"]
        form.correo.data = cliente["correo"]
        form.telefono.data = cliente["telefono"]
        form.estado.data = cliente["estado"]

    return render_template(
        "formulario_cliente.html",
        form=form,
        titulo="Editar cliente"
    )


# =========================================================
# CLIENTES - ELIMINAR
# =========================================================

@app.route(
    "/clientes/eliminar/<int:id>",
    methods=["POST"]
)
@login_required
def eliminar_cliente(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM clientes
            WHERE id = %s
            """,
            (id,)
        )

        conexion.commit()

        flash(
            "Cliente eliminado correctamente.",
            "success"
        )

    except psycopg2.errors.ForeignKeyViolation:

        conexion.rollback()

        flash(
            "No se puede eliminar este cliente porque está relacionado con una factura.",
            "danger"
        )

    finally:

        cursor.close()
        conexion.close()

    return redirect(
        url_for("clientes")
    )


# =========================================================
# PROVEEDORES - LISTAR
# =========================================================

@app.route("/proveedores")
@login_required
def proveedores():

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT
            id,
            nombre,
            correo,
            telefono,
            estado
        FROM proveedores
        ORDER BY id DESC
        """
    )

    proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


# =========================================================
# PROVEEDORES - NUEVO
# =========================================================

@app.route(
    "/proveedores/nuevo",
    methods=["GET", "POST"]
)
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO proveedores
            (
                nombre,
                correo,
                telefono,
                estado
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.correo.data,
                form.telefono.data,
                form.estado.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("proveedores")
        )

    return render_template(
        "formulario_proveedor.html",
        form=form,
        titulo="Nuevo proveedor"
    )


# =========================================================
# PROVEEDORES - EDITAR
# =========================================================

@app.route(
    "/proveedores/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar_proveedor(id):

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT
            id,
            nombre,
            correo,
            telefono,
            estado
        FROM proveedores
        WHERE id = %s
        """,
        (id,)
    )

    proveedor = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not proveedor:

        flash(
            "Proveedor no encontrado.",
            "danger"
        )

        return redirect(
            url_for("proveedores")
        )

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE proveedores
            SET
                nombre = %s,
                correo = %s,
                telefono = %s,
                estado = %s
            WHERE id = %s
            """,
            (
                form.nombre.data,
                form.correo.data,
                form.telefono.data,
                form.estado.data,
                id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Proveedor actualizado correctamente.",
            "success"
        )

        return redirect(
            url_for("proveedores")
        )

    elif not form.is_submitted():

        form.nombre.data = proveedor["nombre"]
        form.correo.data = proveedor["correo"]
        form.telefono.data = proveedor["telefono"]
        form.estado.data = proveedor["estado"]

    return render_template(
        "formulario_proveedor.html",
        form=form,
        titulo="Editar proveedor"
    )


# =========================================================
# PROVEEDORES - ELIMINAR
# =========================================================

@app.route(
    "/proveedores/eliminar/<int:id>",
    methods=["POST"]
)
@login_required
def eliminar_proveedor(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM proveedores
        WHERE id = %s
        """,
        (id,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    flash(
        "Proveedor eliminado correctamente.",
        "success"
    )

    return redirect(
        url_for("proveedores")
    )


# =========================================================
# OPCIONES DE FACTURACIÓN
# =========================================================

def cargar_opciones_factura(form):

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    # CLIENTES
    cursor.execute(
        """
        SELECT
            id,
            nombre
        FROM clientes
        ORDER BY nombre
        """
    )

    clientes = cursor.fetchall()

    form.cliente_id.choices = [
        (
            cliente["id"],
            cliente["nombre"]
        )
        for cliente in clientes
    ]

    # PRODUCTOS
    cursor.execute(
        """
        SELECT
            id,
            nombre
        FROM productos
        ORDER BY nombre
        """
    )

    productos = cursor.fetchall()

    form.producto_id.choices = [
        (
            producto["id"],
            producto["nombre"]
        )
        for producto in productos
    ]

    cursor.close()
    conexion.close()


# =========================================================
# FACTURACIÓN - LISTAR CON JOIN
# =========================================================

@app.route("/facturacion")
@login_required
def facturacion():

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT
            f.id,
            f.numero,
            c.nombre AS cliente,
            p.nombre AS producto,
            f.fecha,
            f.total,
            f.estado
        FROM facturas f
        INNER JOIN clientes c
            ON f.cliente_id = c.id
        INNER JOIN productos p
            ON f.producto_id = p.id
        ORDER BY f.id DESC
        """
    )

    facturas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


# =========================================================
# FACTURACIÓN - NUEVA
# =========================================================

@app.route(
    "/facturacion/nueva",
    methods=["GET", "POST"]
)
@login_required
def nueva_factura():

    form = FacturacionForm()

    cargar_opciones_factura(form)

    if form.validate_on_submit():

        conexion = obtener_conexion()

        cursor = conexion.cursor(
            cursor_factory=RealDictCursor
        )

        # Buscar nombre del cliente
        cursor.execute(
            """
            SELECT nombre
            FROM clientes
            WHERE id = %s
            """,
            (form.cliente_id.data,)
        )

        cliente = cursor.fetchone()

        if not cliente:

            cursor.close()
            conexion.close()

            flash(
                "El cliente seleccionado no existe.",
                "danger"
            )

            return redirect(
                url_for("nueva_factura")
            )

        cursor.execute(
            """
            INSERT INTO facturas
            (
                numero,
                cliente,
                cliente_id,
                producto_id,
                fecha,
                total,
                estado
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                form.numero.data,
                cliente["nombre"],
                form.cliente_id.data,
                form.producto_id.data,
                form.fecha.data,
                form.total.data,
                form.estado.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(
            url_for("facturacion")
        )

    return render_template(
        "formulario_facturacion.html",
        form=form,
        titulo="Nueva factura"
    )


# =========================================================
# FACTURACIÓN - EDITAR
# =========================================================

@app.route(
    "/facturacion/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar_factura(id):

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT
            id,
            numero,
            cliente_id,
            producto_id,
            fecha,
            total,
            estado
        FROM facturas
        WHERE id = %s
        """,
        (id,)
    )

    factura = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not factura:

        flash(
            "Factura no encontrada.",
            "danger"
        )

        return redirect(
            url_for("facturacion")
        )

    form = FacturacionForm()

    cargar_opciones_factura(form)

    if form.validate_on_submit():

        conexion = obtener_conexion()

        cursor = conexion.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            SELECT nombre
            FROM clientes
            WHERE id = %s
            """,
            (form.cliente_id.data,)
        )

        cliente = cursor.fetchone()

        if not cliente:

            cursor.close()
            conexion.close()

            flash(
                "El cliente seleccionado no existe.",
                "danger"
            )

            return redirect(
                url_for(
                    "editar_factura",
                    id=id
                )
            )

        cursor.execute(
            """
            UPDATE facturas
            SET
                numero = %s,
                cliente = %s,
                cliente_id = %s,
                producto_id = %s,
                fecha = %s,
                total = %s,
                estado = %s
            WHERE id = %s
            """,
            (
                form.numero.data,
                cliente["nombre"],
                form.cliente_id.data,
                form.producto_id.data,
                form.fecha.data,
                form.total.data,
                form.estado.data,
                id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Factura actualizada correctamente.",
            "success"
        )

        return redirect(
            url_for("facturacion")
        )

    elif not form.is_submitted():

        form.numero.data = factura["numero"]
        form.cliente_id.data = factura["cliente_id"]
        form.producto_id.data = factura["producto_id"]
        form.fecha.data = factura["fecha"]
        form.total.data = factura["total"]
        form.estado.data = factura["estado"]

    return render_template(
        "formulario_facturacion.html",
        form=form,
        titulo="Editar factura"
    )


# =========================================================
# FACTURACIÓN - ELIMINAR
# =========================================================

@app.route(
    "/facturacion/eliminar/<int:id>",
    methods=["POST"]
)
@login_required
def eliminar_factura(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM facturas
        WHERE id = %s
        """,
        (id,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    flash(
        "Factura eliminada correctamente.",
        "success"
    )

    return redirect(
        url_for("facturacion")
    )


# =========================================================
# EJECUTAR APLICACIÓN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )