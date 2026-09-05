from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(
                min=2,
                max=50,
                message="El nombre debe tener entre 2 y 50 caracteres."
            )
        ]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            ("", "Seleccione una categoría"),
            ("Tecnología", "Tecnología"),
            ("Accesorios", "Accesorios"),
            ("Oficina", "Oficina")
        ],
        validators=[
            DataRequired(message="Debe seleccionar una categoría.")
        ]
    )

    precio = DecimalField(
        "Precio",
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(
                min=0.01,
                message="El precio debe ser mayor que 0."
            )
        ]
    )

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(message="El stock es obligatorio."),
            NumberRange(
                min=0,
                message="El stock no puede ser negativo."
            )
        ]
    )

    submit = SubmitField("Guardar producto")