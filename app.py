from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from sqlalchemy import or_, cast, create_engine
from sqlalchemy.types import String
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import db
from models import Producto, User
from forms import ProductoForm, LoginForm, RegistrationForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Configuración de la base de datos
USER_DB = 'postgres'
USER_PASSWORD = '2025'
SERVER_DB = 'localhost'
NAME_DB = 'supermarket'
FULL_URL_DB = f'postgresql://{USER_DB}:{USER_PASSWORD}@{SERVER_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'llave_secreta_mas_segura'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de correo (asegúrate que está ANTES de crear la instancia de Mail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')
app.config['MAIL_ASCII_ATTACHMENTS'] = True  # Nueva línea importante


db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Configuración de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#Crear el proyecto en flask  
#CODIGO PRUEBA

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Engine para Pandas
engine = create_engine(FULL_URL_DB)

# Funciones de autenticación

# En app.py, modifica la función send_verification_email:


def send_verification_email(user):
    try:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = serializer.dumps(user.email, salt='email-confirm')
        
        msg = Message('Verifica tu cuenta - Supermarket',
                     recipients=[user.email],
                     charset='utf-8')  # Especificar charset
        
        msg.body = f'''Para verificar tu cuenta, visita el siguiente enlace:
{url_for('verify_email', token=token, _external=True)}

Este enlace expirará en 24 horas.
'''
        # Configuración especial para manejar autenticación
        with mail.connect() as conn:
            conn.send(msg)
        
        return True
    except Exception as e:
        app.logger.error(f"Error al enviar correo: {str(e)}")
        
        # En modo desarrollo, mostrar el token directamente
        if app.debug:
            verification_url = url_for('verify_email', token=token, _external=True)
            app.logger.info(f"URL de verificación (solo desarrollo): {verification_url}")
            flash(f'En modo desarrollo: <a href="{verification_url}">Haz clic aquí para verificar</a>', 'info')
            return True
            
        return False

# Rutas de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.is_verified:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('inicio'))
            else:
                flash('Por favor verifica tu cuenta primero. Revisa tu correo electrónico.', 'warning')
        else:
            flash('Correo electrónico o contraseña incorrectos', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_verified=False
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        send_verification_email(user)
        flash('¡Registro exitoso! Por favor verifica tu correo electrónico para activar tu cuenta.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/verify_email/<token>')
def verify_email(token):
    try:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='email-confirm', max_age=86400)
    except:
        flash('El enlace de verificación es inválido o ha expirado.', 'danger')
        return redirect(url_for('login'))
    
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        flash('La cuenta ya está verificada. Por favor inicia sesión.', 'info')
    else:
        user.is_verified = True
        db.session.commit()
        flash('¡Cuenta verificada exitosamente! Ahora puedes iniciar sesión.', 'success')
    
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))

# Rutas protegidas
@app.route('/', methods=['GET'])
@login_required
def inicio():
    query = request.args.get('buscar', '').strip()
    filtro = request.args.get('filtro', 'Nombre')
    
    if query:
        if filtro == 'ID':
            objProducto = Producto.query.filter(
                cast(Producto.id, String).ilike(f"%{query}%")
            ).order_by(Producto.id).all()
        else:
            objProducto = Producto.query.filter(
                Producto.nombre.ilike(f"%{query}%")
            ).order_by(Producto.id).all()
    else:
        objProducto = Producto.query.order_by(Producto.id).all()
    
    total_productos = len(objProducto)
    return render_template('index.html', total=total_productos, datos=objProducto, buscar=query, filtro=filtro)

""" @app.route('/', methods=['GET'])
def inicio():
    query = request.args.get('buscar', '').strip()
    filtro = request.args.get('filtro', 'Nombre')  # Valor por defecto

    if query:
        if filtro == 'ID':
            objProducto = Producto.query.filter(
                cast(Producto.id, String).ilike(f"%{query}%")
            ).order_by(Producto.id).all()
        else:  # Nombre por defecto
            objProducto = Producto.query.filter(
                Producto.nombre.ilike(f"%{query}%")
            ).order_by(Producto.id).all()
    else:
        objProducto = Producto.query.order_by(Producto.id).all()

    total_productos = len(objProducto)
    return render_template('index.html', total=total_productos, datos=objProducto, buscar=query, filtro=filtro) """

@app.route('/curso/<int:id>')
def verProducto(id):
    buscar = request.args.get('buscar', '')
    filtro = request.args.get('filtro', 'Nombre')
    objDosProducto = Producto.query.get(id)
    return render_template('curso.html', dato=objDosProducto, buscar=buscar, filtro=filtro)

@app.route('/insertar-producto', methods=['GET', 'POST'])
def insertarProducto():
    objInsertarProducto = Producto()
    objForm = ProductoForm(obj = objInsertarProducto)

    if request.method == 'POST':
        #Aqui mando a guardar lo que se envia en el POST
        if objForm.validate_on_submit():
            objForm.populate_obj(objInsertarProducto)
            db.session.add(objInsertarProducto)
            db.session.commit()
            return redirect(url_for('inicio'))
        
    return render_template('insertar-producto.html', formulario = objForm)

@app.route('/editar-curso/<int:id>', methods=['GET', 'POST'])
def editarProducto(id):
    buscar = request.args.get('buscar', '')
    filtro = request.args.get('filtro', 'Nombre')
    objEditarProducto = Producto.query.get_or_404(id)
    objDosForm = ProductoForm(obj=objEditarProducto)

    if request.method == 'POST':
        if objDosForm.validate_on_submit():
            objDosForm.populate_obj(objEditarProducto)
            db.session.commit()
            return redirect(url_for('inicio', buscar=buscar, filtro=filtro))
    
    return render_template('editar-curso.html', formulario=objDosForm, buscar=buscar, filtro=filtro)

@app.route('/eliminar-curso/<int:id>')
def eliminarProducto(id):
    objEliminarProducto = Producto.query.get(id)

    db.session.delete(objEliminarProducto)
    db.session.commit()
    
    return redirect(url_for('inicio'))

# =========================
# FUNCIONES PARA GRAFICAR
# =========================

def obtener_tabla_df():
    try:
        consulta = "SELECT id, nombre, categoria, precio, stock FROM public.producto"
        df = pd.read_sql(consulta, engine)
        return df
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return None

def graficar_precio(df):
    plt.figure(figsize=(10, 5))
    sns.histplot(df["precio"], bins=15, kde=True, color="skyblue")
    plt.xlabel("Precio")
    plt.ylabel("Frecuencia")
    plt.title("Distribución de Precios")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def graficar_stock(df):
    # Ordenar por stock descendente y tomar solo los 10 productos más altos
    top_productos = df.sort_values(by="stock", ascending=False).head(10).copy()
    
    # Acortar nombres demasiado largos
    top_productos["nombre"] = top_productos["nombre"].apply(lambda x: x[:20] + "..." if len(x) > 20 else x)

    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_productos, x="nombre", y="stock", hue="nombre", dodge=False, palette="coolwarm", legend=False)
    plt.title("Top 10 productos con mayor stock")
    plt.xlabel("Producto")
    plt.ylabel("Stock")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def graficar_precio_promedio_por_categoria(df):
    plt.figure(figsize=(10, 5))
    promedio = df.groupby("categoria")["precio"].mean().reset_index()
    sns.barplot(data=promedio, x="categoria", y="precio", palette="viridis")
    plt.title("Precio Promedio por Categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Precio Promedio")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Ejecutar para pruebas fuera de Flask
if __name__ == "__main__":
    df_tablas = obtener_tabla_df()
    if df_tablas is not None:
        print(df_tablas.head())
        graficar_precio(df_tablas)
        graficar_stock(df_tablas)
        graficar_precio_promedio_por_categoria(df_tablas)
