from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired(message="El número de factura es obligatorio."),
            Length(
                min=5,
                max=20,
                message="El número de factura debe tener entre 5 y 20 caracteres."
            )
        ]
    )

    cliente = StringField(
        "Cliente",
        validators=[
            DataRequired(message="El cliente es obligatorio."),
            Length(
                min=3,
                max=60,
                message="El nombre del cliente debe tener entre 3 y 60 caracteres."
            )
        ]
    )

    fecha = DateField(
        "Fecha",
        format="%Y-%m-%d",
        validators=[
            DataRequired(message="La fecha es obligatoria.")
        ]
    )

    total = DecimalField(
        "Total",
        validators=[
            DataRequired(message="El total es obligatorio."),
            NumberRange(
                min=0.01,
                message="El total debe ser mayor que 0."
            )
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("", "Seleccione un estado"),
            ("Pagada", "Pagada"),
            ("Pendiente", "Pendiente")
        ],
        validators=[
            DataRequired(message="Debe seleccionar un estado.")
        ]
    )

    submit = SubmitField("Guardar factura")