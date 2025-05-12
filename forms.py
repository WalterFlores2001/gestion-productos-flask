from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo, Length
from wtforms import ValidationError
from models import User

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[DataRequired()])
    categoria = StringField('Categoría', validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0.01, message="El precio debe ser mayor a 0")])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0, message="El stock no puede ser negativo")])
    enviar = SubmitField('Agregar Producto')

class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[
        DataRequired(),
        Length(min=4, max=20, message="El nombre de usuario debe tener entre 4 y 20 caracteres")
    ])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres")
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(),
        EqualTo('password', message="Las contraseñas deben coincidir")
    ])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nombre de usuario ya está en uso. Por favor elige otro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este correo electrónico ya está registrado.')