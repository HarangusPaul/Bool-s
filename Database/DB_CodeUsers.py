import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('D:/Scoala/Bool-s/Database/bools-db-firebase-adminsdk-tsrw7-9299478109.json')

firebase_admin.initialize_app(cred)
db = firestore.client()


def create_Questionnaire(IdUser, IdQuestion, IdAnswer):
    doc_ref_User = db.collection("Users").document(IdUser).collection("Questionnaire").document(IdUser)

    doc_ref_User.set({
        # u"IdUser": IdUser,
        u'IdQuestion': IdQuestion,
        u"IdAnswer": IdAnswer
    })


def create_UsersPassions(IdUser, IdPassion):
    doc_ref_User = db.collection("Users").document(IdUser).collection("UserPassions").document(IdUser)

    doc_ref_User.set({
        # u"IdUser": IdUser,
        u"IdPassion": IdPassion
    })


def create_FacialRecognition(IdUser, IdFacePart, DistanceValue):
    doc_ref_User = db.collection("Users").document(IdUser).collection("FacialRecognition").document(IdUser)

    doc_ref_User.set({
        # u"IdUser": IdUser,
        u"IdFacePart": IdFacePart,
        u"DistanceValue": DistanceValue
    })


def create_NewUser(IdUser,Password, Full_Name, Age, Gmail, IdQuestion, IdAnswer, IdPassion, IdFacePart, DistanceValue):
    doc_ref_User = db.collection("Users").document(IdUser)

    doc_ref_User.set({
        # u"ID": IdUser,
        u'Full_Name': Full_Name,
        u'Password': Password,
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
        if user.get('Full_Name') == UserName:
            password = user.get('Password')
            return password