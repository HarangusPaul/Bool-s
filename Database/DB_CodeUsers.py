import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('D:/Scoala/Bool-s/Database/bools-db-firebase-adminsdk-tsrw7-9299478109.json')

firebase_admin.initialize_app(cred)
db = firestore.client()


def create_Questionnaire(IdUser, Question, Answer):
    doc_ref_User = db.collection("Users").document(IdUser).collection("Questionnaire").document(IdUser)

    doc_ref_User.set({
        u'Text': Question,
        u"Answer": Answer
    })


def create_UsersPassions(IdUser, IdPassion):
    doc_ref_User = db.collection("Users").document(IdUser).collection("UserPassions").document(IdUser)

    doc_ref_User.set({
        # u"IdUser": IdUser,
        u"IdPassion": IdPassion
    })


def create_FacialRecognition(IdUser, Description, DistanceValue):
    doc_ref_User = db.collection("Users").document(IdUser).collection("FacialRecognition").document(IdUser)

    doc_ref_User.set({
        # u"IdUser": IdUser,
        u"Description": Description,
        u"FacialValue": DistanceValue
    })


def create_NewUser(IdUser, Full_Name, Age,Gender,Password, Gmail, IdQuestion, IdAnswer, IdPassion, IdFacePart, DistanceValue):
    doc_ref_User = db.collection("Users").document(IdUser)

    doc_ref_User.set({
        # u"ID": IdUser,
        u'UserName':IdUser,
        u'Full_Name': Full_Name,
        u'Password': Password,
        u'Gender': Gender,
        u"Age": Age,
        u"Gmail": Gmail
    })

    create_Questionnaire(IdUser, IdQuestion, IdAnswer)

    create_UsersPassions(IdUser, IdPassion)

    create_FacialRecognition(IdUser, IdFacePart, DistanceValue)


def update(IdUser, Field, Value, SubColection):
    if (SubColection != '\0'):
        doc_ref_User = db.collection("Users").document(IdUser).collection(SubColection).document(IdUser)

        doc_ref_User.update({
            Field: Value
        })
    else:
        doc_ref_User = db.collection("Users").document(IdUser)
        doc_ref_User.update({
            Field: Value
        })

def database_GetPassword(UserName):
    emp_ref = db.collection('Users')
    docs = emp_ref.stream()

    for doc in docs:
        user = doc.to_dict()
        username = str(user.get('UserName'))
        if username == UserName:
            password = user.get('Password')
            return password

def validate_existence(UserName):
    emp_ref = db.collection('Users')
    docs = emp_ref.stream()

    for doc in docs:
        user = doc.to_dict()
        username = str(user.get('UserName'))
        if username == str(UserName):
            return 1
    return 0

def send_Text_Answer(IdUser,Text):
    doc_ref_User = db.collection("Users").document(IdUser).collection("Questionnaire").document(IdUser)

    doc_ref_User.update({
        "IdAnswer": Text
    })

def send_Facial_Answer(IdUser,Text):
    doc_ref_User = db.collection("Users").document(IdUser).collection("FacialRecognition").document(IdUser)

    doc_ref_User.update({
        "FacialValue": Text
    })

def database(Username):
    emp_ref = db.collection('Users')
    docs = emp_ref.stream()

    for doc in docs:
        user = doc.to_dict()
        username = str(user.get('UserName'))
        if username == Username:
            return user


