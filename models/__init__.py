import enum
from sqlalchemy import (
    Boolean,
    create_engine,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Text,
    Integer,
    String
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.decl_api import DeclarativeMeta

from utils import Env

class Genero(enum.Enum):
    M = 'm'
    F = 'f'

env = Env()

if env.TEST == 'true':
    engine  = create_engine("sqlite:///db/test.db")
    Session = sessionmaker(bind = engine)
    session = Session()

    session.add = lambda _: None
    session.commit = lambda: None
    session.delete = lambda _: None
else:
    engine  = create_engine(env.URLPOSTGRESQL)
    Session = sessionmaker(bind = engine)
    session = Session()

Base: DeclarativeMeta = declarative_base()

class Link(Base):
    __tablename__ = "link"

    id    = Column(Integer, primary_key = True)
    value = Column(String(length = 300), unique = True, nullable = False)
    write = Column(Boolean, nullable = False)

    project_id = Column(Integer, ForeignKey('project.id', ondelete = 'CASCADE'), nullable = False)
    token_id   = Column(Integer, ForeignKey('token.id', ondelete = 'CASCADE'), nullable = False)

    project = relationship("Project")
    token   = relationship('Token')

class Author(Base):
    __tablename__ = "author"

    id     = Column(Integer, primary_key = True)
    name   = Column(String(length = 50), nullable = False)
    email  = Column(String(length = 250), nullable = False)
    birth  = Column(Date, nullable = False)
    gender = Column(Enum(Genero), nullable = False)

    project_id = Column(Integer, ForeignKey("project.id", ondelete='CASCADE'), nullable = False)
    token_id   = Column(Integer, ForeignKey('token.id', ondelete = 'CASCADE'), nullable = False)

    project = relationship("Project")
    token   = relationship('Token')

class Project(Base):
    __tablename__ = "project"

    id           = Column(Integer, primary_key = True)
    title        = Column(String(length = 200), nullable = False)
    description  = Column(Text, nullable = False)
    budget       = Column(Float)
    started      = Column(Date)
    is_completed = Column(Boolean, default = False, nullable = False)

    admin_id = Column(Integer, ForeignKey("user.id", ondelete = 'CASCADE'), nullable = False)
    token_id = Column(Integer, ForeignKey('token.id', ondelete = 'CASCADE'), nullable = False)
    
    admin   = relationship("User")
    token   = relationship('Token')
    authors = relationship(Author, cascade = 'all, delete-orphan')
    links   = relationship(Link, cascade = 'all, delete-orphan')

class User(Base):
    __tablename__ = "user"

    id          = Column(Integer, primary_key = True)
    name        = Column(String(length = 50), nullable = False)
    password    = Column(String(length = 300), nullable = False)
    email       = Column(String(length = 250), unique = True, nullable = False)
    is_admin    = Column(Boolean, nullable = False)
    is_active   = Column(Boolean, default = False, nullable = False)
    last_login  = Column(DateTime)
    date_joined = Column(DateTime, nullable = False)

    token_id    = Column(Integer, ForeignKey('token.id', ondelete = 'CASCADE'), unique = True, nullable = False)

    token    = relationship('Token')
    projects = relationship(Project, cascade = 'all, delete-orphan')

class Token(Base):
    __tablename__ = "token"

    id    = Column(Integer, primary_key = True)
    value = Column(String(length = 300), unique = True, nullable = False)

    users = relationship(User, cascade = 'all, delete-orphan')

Base.metadata.create_all(engine)
