"""
Building a Flask app
"""
from flask import Flask, render_template, request, make_response, jsonify
from flask import session
from flask_cors import CORS
from cohereChatbot.cohereAI import invoke_model as model
from handleModules import handle_signup, handle_login, handle_logout, handle_request, get_pending
from handleModules import handle_admin_login, handle_admin_logout, handle_user_retrival, assign_task, view_task, set_result, view_result
from handleModules import handle_employee_retrival, get_services, get_profile
from handleCrypto import encrypt_text, decrypt_text
from flask_mail import Mail, Message
import uuid
import json


app = Flask(__name__)
CORS(app)
app.secret_key = str(uuid.uuid4())[:50]
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = ''# Your Email
app.config['MAIL_PASSWORD'] = ''# Your Password

mail = Mail(app)


@app.route('/')
def index():
    return render_template('test.html')


@app.route('/encrypt', methods=["POST"])
def encrypt():
    data = request.get_json()
    cypher_txt = encrypt_text(data["msg"], data["password"])
    msg = Message('Nova ',
                  sender='novaNoReply@gmail.com',
                  recipients=[data["email"]])
    msg.body = "This email was sent from Nova."
    msg.html = f"<h1>Your encrypted message</h1><p>{cypher_txt}.</p>"
    mail.send(msg)
    return {"cypher_txt": cypher_txt, "status": True}


@app.route('/decrypt', methods=["POST"])
def decrypt():
    data = request.get_json()
    normal_txt = decrypt_text(data["msg"], data["password"])
    msg = Message('Nova ',
                  sender='novaNoReply@gmail.com',
                  recipients=[data["email"]])
    msg.body = "This email was sent from Nova."
    msg.html = f"<h1>Your decrypted message</h1><p>{normal_txt}.</p>"
    mail.send(msg)
    return {"normal_txt": normal_txt}


@app.route('/AI', methods=["POST"])
def AI():
    result = request.get_json()
    text = result["humanMsg"]
    AI_message = model(text, 'abe1')
    data = {"AImsg": AI_message.content}
    return data


@app.route('/signup', methods=["POST"])
def signup():
    userID = handle_signup()
    return userID


@app.route('/client_signin', methods=["POST"])
def client_signin():
    userData = handle_login(True)
    return userData


@app.route('/employee_signin', methods=["POST"])
def employee_signin():
    loggedIn = handle_login(False)
    return {"ID": session["E_id"], "status": loggedIn}


@app.route('/client_logout', methods=["GET", "POST"])
def client_logout():
    handle_logout(True)
    return render_template('test.html', status=session["U_id"])


@app.route('/employee_logout', methods=["GET", "POST"])
def employee_logout():
    handle_logout(False)
    return render_template('test.html', status2=session["E_id"])


@app.route('/get_services', methods=["POST", "GET"])
def get_service():
    data = get_services()
    #print(data)
    return data


@app.route('/request', methods=["POST"])
def Request():
    pending_id = handle_request()
    return {"P_id": pending_id}


@app.route('/view_pending', methods=["POST", "GET"])
def view_pending():
    data = get_pending(False)
    print(data)
    return data


@app.route('/admin_login', methods=["POST"])
def admin_login():
    loggedIN = handle_admin_login()
    return loggedIN


@app.route('/admin_logout', methods=["POST"])
def admin_logout():
    handle_admin_logout()
    return render_template('test.html', status2=session["A_id"])


@app.route('/retrive_users', methods=["POST", "GET"])
def admin_view_users():
    users = handle_user_retrival()
    return users


@app.route('/retrive_employees', methods=["POST", "GET"])
def admin_view_employees():
    users = handle_employee_retrival()
    return users


@app.route('/admin_view_pending', methods=["POST", "GET"])
def admin_view():
    data = get_pending(True)
    return data



@app.route('/assign_task', methods=["POST"])
def assignTask():
    status = assign_task()
    return status

"""
@app.route('/view_task', methods=["POST", "GET"])
def employee_view_task():
    #handle_login(False)
    print(session)
    result = request.get_json()
    data = view_task(result["E_id"])
    #data = view_task(session["E_id"])
    return data
"""

@app.route('/set_result', methods=["POST", "GET"])
def setTask():
    data = request.get_json()
    print(data)
    email = set_result()
    try:
        msg = Message('Nova ',
                      sender='novaNoReply@gmail.com',
                      recipients=[email])
        msg.body = "This is a test email sent from Flask."
        msg.html = f"<h1>Your Report</h1><h3>{data['P_id']}</h3><p>{data['r_data']}.</p>"
        mail.send(msg)
        return 'Email sent!'
    except Exception as e:
        return f'Error sending email: {str(e)}'


@app.route('/view_result', methods=["POST"])
def viewResult():
    handle_login(True)
    data = view_result(session["U_id"])
    return render_template('test.html', view_result=data)


@app.route('/get_profile', methods=["POST", "GET"])
def getProfile():
    data = get_profile()
    return data



if __name__ == "__main__":
    app.run(debug=True)
