from flask import Flask,render_template,request
from passlib.hash import pbkdf2_sha256
from Database.DB_CodeUsers import database_GetPassword
from Database.DB_CodeUsers import validate_existence
from Database.DB_CodeUsers import create_NewUser
from Ai.API_AI_text import transmitdata
from Database.DB_CodeUsers import send_Text_Answer,database,send_Facial_Answer
import webbrowser
from Interfata.User import User
from werkzeug.utils import secure_filename
import sys, os
from Ai.ApiFacial import file_user

def encrypt_password(password):
    return pbkdf2_sha256.hash(password)


def validate(UserName,Password):
        string = database_GetPassword(UserName)
        if pbkdf2_sha256.verify(Password, string):
            return 1
        return 0

list_of_errors = ["Username/Password incorect","No username","No password","Password not match"]

app = Flask(__name__)

list_of_logged_users = []

def add_new_user(username,browser):
    New_User = User(browser,username)
    list_of_logged_users.append(New_User)

@app.route("/")
def main():
    for user in list_of_logged_users:
        user_data = request.headers.get('User-Agent')
        if user_data == user.get_browser():
            return render_template("MainFacut.html",n = user.get_user())
    return render_template("HomePage.html")

@app.route("/reg")
def register():
    return render_template("Register.html")

@app.route("/reg",methods=["GET","POST"])
def settingData():
    FullName = request.form['fullname']
    Age = int(request.form['age'])
    try:
        Gender = request.form['Option']
    except Exception as ex:
        return render_template("Register.html",n = "Gender not selected")
    UserName = request.form['username']
    Email = request.form['email']
    Pass1 = request.form['password']
    Pass2 = request.form['password0']
    if Age < 13 or Age > 110:
        return render_template("Register.html",n = "Age not corresspond")
    if Email == "" or FullName == "" or Age == "":
        return render_template("Register.html", n = "Not completed spaces!")
    if Pass1 != Pass2:
        return render_template("Register.html",n = list_of_errors[3])
    if len(Pass1) < 6:
        return render_template("Register.html",n = "A password have atleast 6 characters")
    freespace = validate_existence(UserName)
    if freespace == 1:
        return render_template("Register.html",n = "User already exist!")
    Password = encrypt_password(Pass1)
    create_NewUser(UserName,FullName,Age,Gender,Password,Email,"","","","","")
    return render_template("MainFacut.html",n = UserName)

@app.route("/login")
def login():
    return render_template("py.html")

@app.route('/login',methods=["GET","POST"])
def getingData():
    UserName = request.form['username']
    Password = request.form['password']
    step = validate(UserName,Password)
    if Password == "":
        return render_template('py.html', n=list_of_errors[2])
    if UserName == "":
        return render_template('py.html', n = list_of_errors[1])
    if step == 0:
        return render_template('py.html',n=list_of_errors[0])
    user_data = request.headers.get('User-Agent')
    add_new_user(UserName,user_data)
    return render_template("MainFacut.html",n = UserName)

@app.route("/terms")
def terms():
    return render_template("TermsOfUse.html")

@app.route("/personaldata")
def personal_data():
    return render_template("PersonalData.html")

@app.route("/acc",methods= ["GET","POST"])
def get_acc():
    for user in list_of_logged_users:
        user_data = request.headers.get('User-Agent')
        if user_data == user.get_browser():
            d = database(user.get_user())
            return render_template("Account.html",n = user.get_user() , n3 = user.get_user(),n0 =d['Full_Name'],n1 = d['Age'],n2 = d['Gender'],n4 = d['Gmail'])

@app.route("/scan")
def facial():
    for user in list_of_logged_users:
        user_data = request.headers.get('User-Agent')
        if user_data == user.get_browser():
            return render_template("FacialScanPage.html", n=user.get_user())

@app.route("/scan",methods= ["GET","POST"])
def facial_scan():
    for user in list_of_logged_users:
        user_data = request.headers.get('User-Agent')
        if user_data == user.get_browser():
            username = user.get_user()
    try:
        if request.method == 'POST':
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join("", filename))

            d1 = file_user(str(filename))
            #some work
            send_Facial_Answer(username,d1)
            return render_template("ResultPageScan.html",n = username,n2 = d1)
    except Exception as ex:
        for user in list_of_logged_users:
            user_data = request.headers.get('User-Agent')
            if user_data == user.get_browser():
                return render_template("FacialScanPage.html", n=user.get_user())
@app.route("/questions")
def question():
    user_data = request.headers.get('User-Agent')
    for user in list_of_logged_users:
        if user.get_browser() == user_data:
            return render_template("Questions.html",n1 = user.get_user())
@app.route("/questions",methods=["GET","POST"])
def getquestion():
    Description1 = request.form['d1']
    Description2 = request.form['d2']
    Description3 = request.form['d3']

    try:
        Yes_No1 = str(request.form["yes/no1"])
        Yes_No2 = str(request.form["yes/no2"])
        Yes_No3 = str(request.form["yes/no3"])
        Yes_No4 = str(request.form["yes/no4"])
        Yes_No5 = str(request.form["yes/no5"])
        Yes_No6 = str(request.form["yes/no6"])
    except Exception as ex:
        return render_template("Questions.html",n = "Yes/No:Every entry must be complited")
    try:
        Introvert = request.form["radio"]
    except Exception as ex:
        return render_template("Questions.html", n="Match Words:Every entry must be complited")
    Favmusic = request.form["mw2"]
    try:
        Color = request.form["color"]
    except Exception as ex:
        return render_template("Questions.html", n="Match Words:Every entry must be complited")

    Final_text = Description1 + "." + Description2 + "." + Description3 + "." + Yes_No1 + Yes_No2 + Yes_No3 + Yes_No4 + Yes_No5 + Yes_No6
    Final_text = Final_text + Introvert + "." + Favmusic + "." + Color

    user_data = request.headers.get('User-Agent')
    for user in list_of_logged_users:
        if user.get_browser() == user_data:
            send_Text_Answer(user.get_user(),Final_text)
            return render_template('ResultPageQuestionnaire.html',n1=user.get_user(),n = transmitdata(Final_text))


def start():
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
