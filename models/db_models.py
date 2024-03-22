
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from config import engine

Base = declarative_base()


api_group_association = Table(
    'api_group',
    Base.metadata,
    Column('api_id', Integer, ForeignKey('api.id')),
    Column('group_id', Integer, ForeignKey('group.id'))
)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20))
    email = Column(String(70),unique=True)
    is_writable = Column(Boolean, default=False)
    group_id = Column(Integer, ForeignKey('group.id'))    

class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True, autoincrement=True)
    grp_name = Column(String(50), unique=True)
    users = relationship("User", backref="group")  
    apis = relationship("Api", secondary=api_group_association, back_populates="groups")

class Api(Base):
    __tablename__ = "api"
    id = Column(Integer, primary_key=True)
    base_path = Column(String(100), unique=True)
    groups = relationship("Group", secondary=api_group_association, back_populates="apis")
    
Base.metadata.create_all(engine)