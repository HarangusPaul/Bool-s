from flask import Flask,render_template,request
from passlib.context import CryptContext
from Database.DB_CodeUsers import database_GetPassword

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def encrypt_password(password):
    return pwd_context.hash(password)


def validate(UserName,Password):
        string = database_GetPassword(UserName)
        if string == encrypt_password(Password):
            return 1
        return 0

list_of_errors = ["Username/Password incorect","No username","No password"]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("HomePage.html")

@app.route("/reg")
def register():
    return render_template("Register.html")

@app.route("/reg",methods=["GET","POST"])
def settingData():
    FullName = request.form['fullname']
    try:
        Age = int(request.form['age'])
    except Exception as ex:
        return render_template("Register.html",n = "Age empty")
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
    create_NewUser(UserName,FullName,Age,Password,Email,"","","","","")
    return render_template("after.html",n = "succes")

@app.route("/login")
def login():
    return render_template("LogIninterfata.html")

@app.route('/login',methods=["GET","POST"])
def getingData():
    UserName = request.form["username"]
    Password = request.form['password']
    step = validate(UserName,Password)
    if Password == "":
        return render_template('LogIninterfata.html', n = "No entry set")
    if UserName == "":
        return render_template('LogIninterfata.html', n = "No entry set")
    if step == 0:
        return render_template('LogIninterfata.html', n=list_of_errors[0])
    #return render_template('after.html',n = 'Succes')

@app.route("/questions")
def question():
    return render_template("Questions.html")

@app.route("/questions",methods=["GET","POST"])
def getquestion():
    Description1 = request.form['d1']
    Description2 = request.form['d2']
    Description3 = request.form['d3']

    try:
        Yes_No1 = request.form["yes/no1"]
        Yes_No2 = request.form["yes/no2"]
        Yes_No3 = request.form["yes/no3"]
        Yes_No4 = request.form["yes/no4"]
        Yes_No5 = request.form["yes/no5"]
        Yes_No6 = request.form["yes/no6"]
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
    return render_template("Questions.html",n="Succes")

if (__name__ == "__main__"):
    app.run(debug=True)