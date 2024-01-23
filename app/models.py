from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


class DatabaseCredentials(Base):
    __tablename__ = 'database_credentials'
    id = Column(Integer, primary_key=True)
    user = Column(String(80))
    _password_hash = Column("password", String(256))  # Store hashed password
    host = Column(String(80))
    dbname = Column(String(80))
    port = Column(Integer)

    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, plaintext):
        self._password_hash = generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return check_password_hash(self._password_hash, plaintext)
