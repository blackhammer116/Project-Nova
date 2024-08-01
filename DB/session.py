#!/usr/bin/python3

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model import Client, Admin, Pending, Service, Employee, Result, Base

engine = create_engine('mysql+mysqldb://admin:admin123@localhost:1123/nova')

Session = sessionmaker(bind=engine)

session = Session()

session.close()
engine.dispose()
