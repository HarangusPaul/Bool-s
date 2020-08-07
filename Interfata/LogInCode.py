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
    return render_template("LogInInterfata.html.html")

@app.route('/',methods=["GET","POST"])
def getingData():
    UserName = request.form['username']
    Password = request.form['password']
    step = validate(UserName,Password)
    if Password == "":
        return render_template('LogInInterfata.html', n=list_of_errors[2])
    if UserName == "":
        return render_template('LogInInterfata.html', n = list_of_errors[1])
    if step == 0:
        return render_template('LogInInterfata.html',n=list_of_errors[0])
    return render_template('after.html',n = 'Succes')

if (__name__ == "__main__"):
    app.run(debug=True)