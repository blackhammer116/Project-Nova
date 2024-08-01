-- Database for Project Nova

-- Create database
CREATE DATABASE nova;

-- Select a database
USE nova;

-- Creating Users table
CREATE TABLE client(U_id varchar(50) NOT NULL PRIMARY KEY, f_name varchar(150) NOT NULL, l_name varchar(150) NOT NULL, m_name varchar(150) NULL, dob date NOT NULL, p_number varchar(255) NOT NULL, email varchar(250) NOT NULL, username varchar(150) NOT NULL, password varchar(150) NOT NULL, credit_number varchar(256) NULL, R_id varchar(50) NULL);

-- Creating Pending table
CREATE TABLE pending(P_id varchar(50) NOT NULL PRIMARY KEY, s_data varchar(250) NOT NULL, U_id varchar(50) NOT NULL, S_id varchar(50) NOT NULL);

-- Creating Services table
CREATE TABLE service(S_id varchar(50) NOT NULL PRIMARY KEY, s_name varchar(250) NOT NULL, A_id varchar(50) NULL);

-- Creating Admin table
CREATE TABLE admin(A_id varchar(50) NOT NULL PRIMARY KEY, f_name varchar(150) NOT NULL, l_name varchar(150) NOT NULL, m_name varchar(150) NULL, dob date NOT NULL, p_number varchar(255) NOT NULL, email varchar(250) NOT NULL, username varchar(150) NOT NULL, password varchar(150) NOT NULL, P_id varchar(50) NULL);

-- Creating Employee table
CREATE TABLE employee(E_id varchar(50) NOT NULL PRIMARY KEY, f_name varchar(150) NOT NULL, l_name varchar(150) NOT NULL, m_name varchar(150) NULL, dob date NOT NULL, p_number varchar(255) NOT NULL, email varchar(250) NOT NULL, username varchar(150) NOT NULL, password varchar(150) NOT NULL, P_id varchar(50) NULL);

-- Creating Results table
CREATE TABLE result(R_id varchar(50) NOT NULL PRIMARY KEY, r_data varchar(350) NOT NULL, E_id varchar(50) NOT NULL, U_id varchar(50) NOT NULL);

-- Adding foreign key constraint
ALTER TABLE client
  ADD CONSTRAINT client_ibfk_1 FOREIGN KEY (R_id) REFERENCES result(R_id);

ALTER TABLE pending
  ADD CONSTRAINT pending_ibfk_1 FOREIGN KEY (U_id) REFERENCES client(U_id),
  ADD CONSTRAINT pending_ibfk_2 FOREIGN KEY (S_id) REFERENCES service(S_id);

ALTER TABLE service
  ADD CONSTRAINT service_ibfk_1 FOREIGN KEY (A_id) REFERENCES admin(A_id);

ALTER TABLE admin
  ADD CONSTRAINT admin_ibfk_1 FOREIGN KEY (P_id) REFERENCES pending(P_id);

ALTER TABLE employee
  ADD CONSTRAINT employee_ibfk_1 FOREIGN KEY (P_id) REFERENCES admin(P_id);

ALTER TABLE result
  ADD CONSTRAINT result_ibfk_1 FOREIGN KEY (E_id) REFERENCES employee(E_id),
  ADD CONSTRAINT result_ibfk_2 FOREIGN KEY (U_id) REFERENCES pending(U_id);
