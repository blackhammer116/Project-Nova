#!/usr/bin/python3
"""
Module to Create classes that will reperesent the DB by the use of
SQLAlchemy.

imports: required sqlalchemy modules.
        - uuid for generating unique id for primary keys

Developments: finished creating the classes and mapping them to their
            respective foreign keys
TODO: create relationship with the required table
    - define methods respective to each class
"""
from sqlalchemy import Column, String, Date, Table
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid


Base = declarative_base()


class Client(Base):
    """
    Client: class that defines and operates on client table
    Development: finished defining all the attribute.
               - defined __repr__ method
    TODO: identify what methods it needs
    """
    __tablename__ = 'client'

    U_id = Column(String(50), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4())[:50])
    f_name = Column(String(150), nullable=False)
    l_name = Column(String(150), nullable=False)
    m_name = Column(String(150), nullable=True)
    dob = Column(Date, nullable=False)
    p_number = Column(String(255), nullable=False)
    email = Column(String(250), nullable=False)
    username = Column(String(150), nullable=False)
    password = Column(String(150), nullable=False)
    credit_number = Column(String(256), nullable=True)
    result = relationship('Result', secondary='client_result')
    R_id = Column(String(50), ForeignKey('result.R_id'), nullable=True)# edit this to contain the right foreign key 
    
    def __repr__(self):
        """
        Function for ease of display
        """
        return f"""Client(ID='{self.U_id}', f_name='{self.f_name}', l_name='{self.l_name}', m_name='{self.m_name}', DOB={self.dob}, p_number='{self.p_number}', email='{self.email}',username = '{self.username}', password = '{self.password}', credit_number = '{self.credit_number}')\n"""



class Pending(Base):
    """
    Pending: A class inheriting from Base, used to define and operate on
            pending table
    Development: finished Attribute and relationship definition
    TODO: define methods associated with this class
    """
    __tablename__ = 'pending'
     
    P_id = Column(String(50), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4())[:50])
    s_data = Column(String(250), nullable=False)
    U_id = Column(String(50), ForeignKey('client.U_id'), nullable=False)
    S_id = Column(String(50), ForeignKey('service.S_id'), nullable=False)# not finished, add reference and relationship
    pending = relationship('Client', backref='user_status')
    employees = relationship('Employee', secondary='employee_pending')
    services = relationship('Service', backref='services')
    
    def __repr__(self):
        """
        Function for ease of display
        """
        return f"""Pending(P_id='{self.P_id}', s_data='{self.s_data}', U_id='{self.U_id}', S_id='{self.S_id}')\n"""


class Service(Base):
    """
    Service: A class inheriting from Base, defines and operates on service
            table.
    Development: finished defining attributes
    TODO: define methods and identify the required relationships
    """
    __tablename__ = 'service'

    S_id = Column(String(50), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4())[:50])
    s_name = Column(String(250), nullable=False)
    s_desc = Column(String(1080), nullable=True)
    A_id= Column(String(50), ForeignKey('admin.A_id'), nullable=True)

    def __repr__(self):
        """
        Function for ease of display
        """
        return f"""Service(ID='{self.S_id}', s_name='{self.s_name}', A_id='{self.A_id}')\n"""


class Admin(Base):
    """
    Admin: A class that inherites from Base, defines and operates on admin table
    Development: finished defining attributes
    TODO: define required methods and identify the relationship
    """
    __tablename__ = 'admin'

    A_id = Column(String(50), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4())[:50])
    f_name = Column(String(150), nullable=False)
    l_name = Column(String(150), nullable=False)
    m_name = Column(String(150), nullable=True)
    dob = Column(Date, nullable=False)
    p_number = Column(String(255), nullable=False)
    email = Column(String(250), nullable=False)
    username = Column(String(150), nullable=False)
    password = Column(String(150), nullable=False)    
    P_id = Column(String(50), ForeignKey('pending.P_id'), nullable=True)
    
    def __repr__(self):
        """
        Function for ease of display
        """
        return f"""Admin(ID='{self.A_id}', f_name='{self.f_name}', l_name='{self.l_name}', m_name='{self.m_name}', DOB={self.dob}, p_number='{self.p_number}', email='{self.email}',username = '{self.username}', password = '{self.password}')\n"""


class Employee(Base):
    """
    Employee: A class that inherites from Base, defines and operates on employee table
    Development: finished defining attributes and some relationships
    TODO: define required methods
    """
    __tablename__ = 'employee'

    E_id = Column(String(50), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4())[:50])
    f_name = Column(String(150), nullable=False)
    l_name = Column(String(150), nullable=False)
    m_name = Column(String(150), nullable=True)
    dob = Column(Date, nullable=False)
    p_number = Column(String(255), nullable=False)
    email = Column(String(250), nullable=False)
    username = Column(String(150), nullable=False)
    password = Column(String(150), nullable=False)
    P_id = Column(String(50), ForeignKey('pending.P_id'), nullable=True)
    pending = relationship('Pending', secondary='employee_pending', overlaps="employees")

    def __repr__(self):
        """
        Function for ease of display
        """
        return f"""Employee(ID='{self.E_id}', f_name='{self.f_name}', l_name='{self.l_name}', m_name='{self.m_name}', DOB={self.dob}, p_number='{self.p_number}', email='{self.email}',username = '{self.username}', password = '{self.password}')\n"""


class Result(Base):
    """
    Result: A class that inherites from Base, defines and operates on result table
    Development: finished defining attributes and relationships
    TODO: define required methods.
    """
    __tablename__ = 'result'
    
    R_id = Column(String(50), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4())[:50])
    r_data = Column(String(350), nullable=False)
    E_id = Column(String(50), ForeignKey('employee.E_id'), nullable=False)
    U_id = Column(String(50), ForeignKey('client.U_id'), nullable=False)
    clients = relationship('Client', secondary="client_result", overlaps="result")
    employees = relationship('Employee', backref='employee', primaryjoin="and_(Result.E_id == Employee.E_id)")
    
    def __repr__(self):
        """
        Function for ease of display
        """
        return f"""Result(ID='{self.R_id}', r_data='{self.r_data}', E_id='{self.E_id}', U_id='{self.U_id}')\n"""


employee_pending = Table(
        'employee_pending', Base.metadata,
        Column('employeeId',String(50), ForeignKey("employee.E_id"), nullable=False),
        Column('pendingId',String(50), ForeignKey("pending.P_id"), nullable=False)
        )


client_result = Table(
        'client_result', Base.metadata,
        Column('clientID',String(50), ForeignKey("client.U_id"), nullable=False),
        Column('resultID',String(50), ForeignKey("result.R_id"), nullable=False)
        )
