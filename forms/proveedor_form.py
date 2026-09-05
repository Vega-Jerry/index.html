from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre del proveedor",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(
                min=3,
                max=60,
                message="El nombre debe tener entre 3 y 60 caracteres."
            )
        ]
    )

    correo = EmailField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    telefono = TelField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(
                min=10,
                max=10,
                message="El teléfono debe tener 10 dígitos."
            )
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("", "Seleccione un estado"),
            ("Activo", "Activo"),
            ("Inactivo", "Inactivo")
        ],
        validators=[
            DataRequired(message="Debe seleccionar un estado.")
        ]
    )

    submit = SubmitField("Guardar proveedor")