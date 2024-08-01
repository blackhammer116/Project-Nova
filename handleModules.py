#from app import app
from flask import request, render_template, make_response, jsonify
from flask import session as webSession
#from cohereChatbot.cohereAI import invoke_model as model
from DB.model import Client, Admin, Pending, Employee, Service, Result, employee_pending
from sqlalchemy import select, update
from DB.session import session
import re
from userData import person_list
import random


def handle_signup():
    """
    handles user/client signup and sets up cookie
    by the user id to maintain user login
    """
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    data = request.get_json()
    newUser = random.choice(person_list)
    isValid = bool(re.match(email_pattern, data["email"]))
    if not isValid:
        return "Error email not valid"

    client = Client(f_name=newUser['f_name'],
                    l_name=newUser['l_name'],
                    m_name=newUser['m_name'],
                    dob=newUser['dob'],
                    p_number=newUser['p_number'],
                    email=data['email'],
                    username=data['username'],
                    password=data['password']
                    )
    session.add(client)
    session.commit()
    webSession['U_id'] = client.U_id
    return {"status": True, "id": client.U_id}


def handle_login(isClient: bool):
    """
    handles user login using username and password
    works for both employee and client
    """
    data = request.get_json()
    if not isClient:
        result = session.query(Employee).filter(
                Employee.username==data["username"]).first()
    else:
        result = session.query(Client).filter(
                Client.username==data["username"]).first()

    if bool(result):
        user = result
        if user.password == data["password"]:
            if not isClient:
                webSession["E_id"] = user.E_id
                return {"status": True, "E_id": webSession["E_id"]}
            else:
                webSession["U_id"] = user.U_id
                return {"status": True, "U_id": webSession["U_id"]}
        else:
            return {"status": False}


def handle_logout(isClient: bool):
    """
    handles user's logout works for both employee and client
    Args:
        isClient: to identify if its a client or employee
    """
    if not isClient:
        webSession.pop("E_id", None)
    else:
        webSession.pop("U_id", None)
    return True

def handle_request():
    """
    handles user request of services and adds them to pending table
    """
    result = request.get_json()
    data = {"IP": result["ip"], "domain": result["domain"]}
    pending = Pending(s_data= data,
                      U_id=result["U_id"],
                      S_id=result["S_id"])
    session.add(pending)
    session.commit()
    return pending.P_id


def get_pending(isAdmin: bool):
    """
    Retrives the list of pending tasks/services from the DB
    for both admin and client
    Args:
        isAdmin: boolean value to check if the user who requested
        this is an admin or client
    """
    #print(request.data)
    userId = request.get_json()
    #print(userId["U_id"])
    if not isAdmin:
        print(userId['U_id'])
        result = session.query(Pending).filter(Pending.U_id==userId["U_id"]).all()
        #print(result)
        #result = session.execute(select(Pending).where(Pending.U_id==webSession["U_id"]))
    else:
        result = session.query(Pending).all()
        #result = session.execute(select(Pending))
    data = []
    for i in range(len(result)):
        data.append({
            "P_id": result[i].P_id,
            "s_data": result[i].s_data,
            "U_id": result[i].U_id,
            "S_id": result[i].S_id
            })
    #print(data)
    return data


def get_profile():
    """
    retrives logged on user's name
    """
    userId = request.get_json()
    name = session.query(Client.f_name, Client.l_name).filter(Client.U_id == userId['id']).first()
    print(name)
    return(name)



def get_services():
    """
    Retrives all the services from the databae
    """
    serviceObj = session.query(Service).all()
    data = []
    for i in range(len(serviceObj)):
        data.append({
            "S_id": serviceObj[i].S_id,
            "s_name": serviceObj[i].s_name,
            "s_desc": serviceObj[i].s_desc,
            })
    #print(data)
    return data


def handle_admin_login():
    """
    handles admin login and validation
    """
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    result = session.query(Admin).filter(Admin.username==username).first()
    print(result)
    if result:
        if result.password == password:
            webSession["A_id"] = result.A_id
            return {"status": True}
        else:
            return {"status": False}


def handle_admin_logout():
    """
    handles admin logout
    """
    webSession.pop("A_id", None)
    return {"Status": True}


def handle_user_retrival():
    """
    handles retrival of user information for the admin
    """
    users = session.query(Client).all()
    data = []
    for i in range(len(users)):
        data.append({"U_id": users[i].U_id,
                     "fname": users[i].f_name,
                     "lname": users[i].l_name,
                     "mname": users[i].m_name,
                     "dob": users[i].dob,
                     "pnumber": users[i].p_number,
                     "email": users[i].email,
                     "username": users[i].username,
                     "password": users[i].password,
                     "credit": users[i].credit_number,
                     "R_id": users[i].R_id
                     })
    return data



def handle_employee_retrival():
    """
    handles retrival of user information for the admin
    """
    users = session.query(Employee).all()
    data = []
    for i in range(len(users)):
        data.append({"E_id": users[i].E_id,
                     "fname": users[i].f_name,
                     "lname": users[i].l_name,
                     "mname": users[i].m_name,
                     "dob": users[i].dob,
                     "pnumber": users[i].p_number,
                     "email": users[i].email,
                     "username": users[i].username,
                     "password": users[i].password,
                     })
    return data


def assign_task():
    """
    This is used for admins to assign tasks/services requests
    to the employee so that the employee may work it
    """
    data = request.get_json()
    print(data["E_id"])
    employee = session.query(Employee).get(data["E_id"])
    print(employee)
    task = session.query(Pending).get(data["P_id"])
    employee.pending.append(task)
    """session.execute(
            update(Employee).where(
                Employee.E_id==request.form["E_id"]
                ).values(P_id=request.form["P_id"])
            )"""
    session.commit()
    return {"status": True}



def view_task(Em_id: str):
    return ''
    """
    Lets employees view their assigned tasks
    Args:
        E_id: employee's unique ID
    """
    """
    try:
        #P_id = session.query(Pending.P_id)\
        #        .join(Pending.employees)\
        #        .join(Employee)\
        #        .filter(Employee.E_id==Em_id)\

        P_id_Obj = session.execute(f"select * from employee_pending where employee_pending.employeeId = '{Em_id}';").scalars()
        print(P_id_Obj.employeeId)
        ""result = []
        for i in P_id:
            result.append(session.query(Pending).filter(Pending.P_id == i).first())""
        #result = session.query(Pending).filter(Pending.P_id.in_(i[0] for i in P_id)).all()
    except:
        session.rollback()
        raise
    ""print(result)
    data = []
    for i in range(len(result)):
        data.append({
            "P_id": result[i].P_id,
            "s_data": result[i].s_data,
            "U_id": result[i].U_id,
            "S_id": result[i].S_id,
            })
    return data""
    return "True"
"""

def set_result():
    """
    Method to set the result of a pending task for user
    Args:
        U_id: user's id
    """
    data = request.get_json()
    result = Result(r_data=data["r_data"], E_id=data["E_id"], U_id=data["U_id"])
    email = session.query(Client.email).filter(Client.U_id==data["U_id"]).first()
    session.add(result)
    client = session.query(Client).get(data["U_id"])
    client.result.append(result)
    """pendingObj = session.get(Pending, request.form["P_id"])
    session.begin_nested()
    session.query(employee_pending).filter(employee_pending.pendingId ==  request.form["P_id"]).first().delete()
    stmt = f"DELETE FROM employee_pending WHERE employee_pending.pendingId = '{pendingObj.P_id}' AND  employee_pending.employeeId='{webSession['E_id']}'"
    session.execute(stmt)
    session.delete(pendingObj)"""

    session.commit()

    return email


def view_result(us_id: str):
    R_id = session.query(Result.R_id)\
            .join(Result.clients)\
            .filter(Client.U_id == us_id)\
            .all()
    data = session.query(Result).filter(Result.R_id.in_(i[0] for i in R_id)).all()
    return data
