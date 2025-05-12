from database import db
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Producto(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    categoria: Mapped[str] = mapped_column(nullable=False)
    precio: Mapped[float] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)

    def __str__(self):
        return (
            f'Id: {self.id}, '
            f'Nombre: {self.nombre}, '
            f'Categoría: {self.categoria}, '
            f'Precio: {self.precio}, '
            f'Stock: {self.stock}'
        )

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'