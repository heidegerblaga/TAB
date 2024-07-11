from sqlalchemy import BigInteger,String,Boolean,Column,Date,ForeignKey,Float,Integer
from psql import engine
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import pandas as pd


Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

dbConnection = engine.connect()

# Read data from PostgreSQL database table and load into a DataFrame instance



class Kontynenty(Base):

    __tablename__='Kontynenty'

    kontynent = mapped_column(String, primary_key=True)
    children = relationship("Kraje", back_populates="Kontynenty")


class Kraje(Base):

    __tablename__="Kraje"


    kraj = mapped_column(String, primary_key=True)
    kontynent = mapped_column(ForeignKey("Kontynenty.kontynent"))
    parent = relationship("Kontynenty", back_populates="Kraje")
    children = relationship("Regiony", back_populates="Kraje")

class Regiony(Base):
    __tablename__ = "Regiony"
    region = Column(String, primary_key=True)
    parent_id = mapped_column(ForeignKey("Kraje.kraj"))
    kraj = relationship("Kraje", back_populates="regiony")
    atrakcje = relationship("Atrakcje", back_populates="region")

# Definicja klasy reprezentującej tabelę 'Atrakcje'
class Atrakcje(Base):
    __tablename__ = "Atrakcje"
    id = Column(BigInteger, primary_key=True)
    parent_id = mapped_column(ForeignKey("Regiony.region"))
    region = relationship("Regiony", back_populates="atrakcje")
    opinie = relationship("Opinie", back_populates="atrakcja")

    atrakcja = Column(String)
    dlugosc = Column(Float)
    szerokosc = Column(Float)

class Redaktorzy(Base):

    __tablename__ = "Redaktorzy"

    id = Column(BigInteger, primary_key=True)
    opinie = relationship("Opinie", back_populates="Redaktorzy")
    haslo = Column(String)
    email = Column(String)


class Opinie(Base):

    __tablename__="Opinie"

    id = Column(BigInteger, primary_key=True)
    parent_id = mapped_column(ForeignKey("Atrakcje.id"))
    redaktor_id = mapped_column(ForeignKey("Redaktorzy.id"))
    opinie = relationship("Redaktorzy", back_populates="Opinie")
    parent = relationship("Atrakcje", back_populates="Opinie")
    opinia = Column(String)


Base.metadata.create_all(engine)


Kontynenty_df = pd.read_sql("SELECT * FROM \"Kontynenty\"", engine)
Kraje_df = pd.read_sql("SELECT * FROM \"Kraje\"", engine)
Regiony_df = pd.read_sql("SELECT * FROM \"Regiony\"", engine)
Atrakcje_df = pd.read_sql("SELECT * FROM \"Atrakcje\"", engine)
Redaktorzy_df = pd.read_sql("SELECT * FROM \"Redaktorzy\"", engine)
Opinie_df = pd.read_sql("SELECT * FROM \"Opinie\"", engine)