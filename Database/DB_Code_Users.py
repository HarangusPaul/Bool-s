import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('bools-db-ae67804c2b63.json')


firebase_admin.initialize_app(cred)
db = firestore.client()


def Add_OverWrite(N_Col,N_Doc):

    doc_ref = db.collection(N_Col).document(N_Doc)
    #Fiind pentru primul tabel v-om seta ID Full_Name Age Gmail
    ID = input("ID:")
    Full_Name = input("Full_Name:")
    Age = input("Age:")
    Gmail = input("Gmail:")
    doc_ref.set({
        "ID" : ID,
        u'Full_Name' : Full_Name,
        "Age" : Age,
        "Gmail" : Gmail
    })


def Update_Data(N_Col,N_Doc):
    doc_ref = db.collection(N_Col).document(N_Doc)

    Field = input("Campul pe care vrei sa il modifici:")
    Value = input("Valoare:")

    doc_ref.update({
        Field : Value
    })
N_Col = input("Numele Colectie:")
N_Doc = input("Numele documentului:")

#Add_OverWrite(N_Col,N_Doc)

#Update_Data(N_Col,N_Doc)