from io import BytesIO
import os
from PIL import Image, ImageDraw
import requests
import math
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import FaceAttributeType
from msrest.authentication import CognitiveServicesCredentials


KEY = '99f1b2d5bb01427fb0f7ec8f1b859a1a'

ENDPOINT = 'https://appelleface.cognitiveservices.azure.com/'

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


def face_scan(face1 : str):

    face_attributes = ['age', 'gender', 'headPose', 'smile', 'facialHair', 'glasses', 'emotion']

    image = open(face1 , 'r+b')
    detected_faces = face_client.face.detect_with_stream(image,return_face_landmarks=True,return_face_attributes=face_attributes)
    if not detected_faces:
        raise Exception(
            'No face detected from image')

    for face in detected_faces:
        eye_left_top = face.face_landmarks.eye_left_top
        eye_left_bottom = face.face_landmarks.eye_left_bottom
        eye_left_outer = face.face_landmarks.eye_left_outer
        eye_left_inner = face.face_landmarks.eye_left_inner
        eye_right_top = face.face_landmarks.eye_right_top
        eye_right_bottom = face.face_landmarks.eye_right_bottom
        eye_right_outer = face.face_landmarks.eye_right_outer
        eye_right_inner = face.face_landmarks.eye_right_inner
        pupil_left = face.face_landmarks.pupil_left
        pupil_right = face.face_landmarks.pupil_right
        nose_tip = face.face_landmarks.nose_tip
        mouth_left = face.face_landmarks.mouth_left
        mouth_right = face.face_landmarks.mouth_right
        eyebrow_left_outer = face.face_landmarks.eyebrow_left_outer
        eyebrow_left_inner = face.face_landmarks.eyebrow_left_inner
        eyebrow_right_inner = face.face_landmarks.eyebrow_right_inner
        eyebrow_right_outer = face.face_landmarks.eyebrow_right_outer
        nose_root_left = face.face_landmarks.nose_root_left
        nose_root_right = face.face_landmarks.nose_root_right
        nose_left_alar_top = face.face_landmarks.nose_left_alar_top
        nose_right_alar_top = face.face_landmarks.nose_right_alar_top
        nose_left_alar_out_tip = face.face_landmarks.nose_left_alar_out_tip
        nose_right_alar_out_tip = face.face_landmarks.nose_right_alar_out_tip
        upper_lip_top = face.face_landmarks.upper_lip_top
        upper_lip_bottom = face.face_landmarks.upper_lip_bottom
        under_lip_top = face.face_landmarks.under_lip_top
        under_lip_bottom = face.face_landmarks.under_lip_bottom
        face_age = face.face_attributes.age
        face_gender = face.face_attributes.gender
        head_pose = face.face_attributes.head_pose
        smile = face.face_attributes.smile
        facial_hair = face.face_attributes.facial_hair
        glasses = face.face_attributes.glasses
        face_emotion = face.face_attributes.emotion
        dicti = {
            'eye_left_top' : eye_left_top,
            'eye_left_bottom' : eye_left_bottom,
            'eye_left_outer' : eye_left_outer,
            'eye_left_inner' : eye_left_inner,
            'eye_right_top' : eye_right_top,
            'eye_right_bottom' : eye_right_bottom,
            'eye_right_outer' : eye_right_outer,
            'eye_right_inner' : eye_right_inner,
            'pupil_left' : pupil_left,
            'pupil_right' : pupil_right,
            'nose_tip' : nose_tip,
            'mouth_left' : mouth_left,
            'mouth_right' : mouth_right,
            'eyebrow_left_outer' : eyebrow_left_outer,
            'eyebrow_left_inner' : eyebrow_left_inner,
            'eyebrow_right_inner' : eyebrow_right_inner,
            'eyebrow_right_outer' : eyebrow_right_outer,
            'nose_root_left' : nose_root_left,
            'nose_root_right' : nose_root_right,
            'nose_left_alar_top' : nose_left_alar_top,
            'nose_right_alar_top' : nose_right_alar_top,
            'nose_left_alar_out_tip' : nose_left_alar_out_tip,
            'nose_right_alar_out_tip' : nose_right_alar_out_tip,
            'upper_lip_top' : upper_lip_top,
            'upper_lip_bottom' : upper_lip_bottom,
            'under_lip_top' : under_lip_top,
            'under_lip_bottom' : under_lip_bottom,
            'face_age' : face_age,
            'face_gender' : face_gender,
            'head_pose' : head_pose,
            'smile' : smile,
            'facial_hair' : facial_hair,
            'glasses' : glasses,
            'face_emotion' : face_emotion
        }

        return dicti


    # def getRectangle(faceDictionary):
    #     rect = faceDictionary.face_rectangle
    #     left = rect.left
    #     top = rect.top
    #     right = left + rect.width
    #     bottom = top + rect.height
    #
    #     return ((left, top), (right, bottom))
    # response = requests.get(image)
    # img = Image.open(BytesIO(response.content))
    #
    # # For each face returned use the face rectangle and draw a red box.
    # print('Drawing rectangle around face... see popup for results.')
    # print()
    # draw = ImageDraw.Draw(img)
    # for face in detected_faces:
    #     draw.rectangle(getRectangle(face), outline='red')
    #
    # img.show()


def file_user(filename):

    location_file = str(filename)
    dicti = face_scan(location_file)

    text = ""

    distanta_intre_pupile = int(math.sqrt(((dicti['pupil_right'].x ** 2) - (dicti['pupil_left'].x ** 2))
                                      + ((dicti['pupil_right'].y ** 2) - (dicti['pupil_left'].y ** 2))))
    marimea_ochi_latura_a = int(math.sqrt((dicti['eye_left_inner'].x ** 2 - dicti['eye_left_outer'].x** 2)
                                      + (dicti['eye_left_inner'].y ** 2 - dicti['eye_left_outer'].y ** 2)))
    marimea_ochi_latura_b = int(math.sqrt((dicti['eye_left_bottom'].x ** 2 - dicti['eye_left_top'].x ** 2)
                                      + (dicti['eye_left_bottom'].y ** 2 - dicti['eye_left_top'].y ** 2)))
    arie = marimea_ochi_latura_a * marimea_ochi_latura_b
    lungimea_gurii = int(math.sqrt((dicti['mouth_right'].x ** 2 - dicti['mouth_left'].x ** 2)
                               + (dicti['mouth_right'].y ** 2 - dicti['mouth_left'].y ** 2)))
    lungimea_sprancenelor_stanga = int(math.sqrt((dicti['eyebrow_left_inner'].x ** 2 - dicti['eyebrow_left_outer'].x ** 2)
                                             + (dicti['eyebrow_left_inner'].y ** 2 - dicti['eyebrow_left_outer'].y ** 2)))
    lungimea_sprancenelor_dreapta = int(math.sqrt((dicti['eyebrow_right_outer'].x ** 2 - dicti['eyebrow_right_inner'].x ** 2)
                                              + (dicti['eyebrow_right_outer'].y ** 2 - dicti['eyebrow_right_inner'].y ** 2)))
    marimea_buzelor_sus = int(math.sqrt((dicti['upper_lip_top'].x - dicti['upper_lip_bottom'].x)**2 + (dicti['upper_lip_top'].y - dicti['upper_lip_bottom'].y)**2 ))
    marimea_buzelor_jos = int(math.sqrt((dicti['under_lip_top'].x - dicti['under_lip_bottom'].x) ** 2 + (dicti['under_lip_top'].y - dicti['under_lip_bottom'].y) ** 2))

    latimea_buzelor = marimea_buzelor_sus + marimea_buzelor_jos

    distanta_sprancene = int(dicti['eyebrow_right_inner'].x - dicti['eyebrow_left_inner'].x)

    distanta_intre_ochi = int(dicti['eye_right_inner'].x - dicti['eye_left_inner'].x)

    distanta_ochi_spranceana = int(dicti['eyebrow_right_inner'].y) - int(dicti['eye_left_inner'].y)

    marimea_nas = int(dicti['nose_root_left'].y) - int(dicti['nose_left_alar_out_tip'].y)
    if distanta_intre_pupile > marimea_ochi_latura_a + 100:
        text = text + "Inseamna ca persoana este neglijenta, indiferenta si da dovada de napasare in modul lor de a se comporta. Sunt lenti in decizii si nu sunt potriviti in activitati care presupun reactii rapide si agerime.\nAu, in schimb, o capacitate foarte mare de memorare, sunt rezistenti, toleranti si foarte meticulosi in ceea ce fac.\n\n"
    else: text = text + "Persoana are o opinie ingusta asupra realitatii si foarte putina toleranta fata de semeni. E greu de multumit, devine rareori obraznic si are asteptari mari de la alti oameni si de la situatiile din viata lor.\nAu, in schimb, capacitatea de a se  concentra foartre bine, sunt buni observatori si obtin rezultate remarcabile in analiza si calcule.\n\n"

    if marimea_buzelor_jos - marimea_buzelor_sus < 6:
        text = text + "Persoana da mai multa atentie\n\n"
    else: text = text + "Persona are nevoie de mai multa atentie.\n\n"


    if marimea_ochi_latura_b > distanta_ochi_spranceana:
        text = text + "Persoana este prietenoasa, se implica foarte puternic in relatoole cu persoanale pe care doresc sa le ajute.\nCu cat sunt mai joase, cu atat sunt mai implicate in aceste relatii.\n\n"
    else: text = text + "Persoana este foarte pretentioasa, are roleranta ridicata, afiseaza un aer aristocratic, rece si detasat. Se spune ca are eleganta si diplomatia innascute.\nIsi fac cu greu prieteni apropiati, prefrand sa mentina o anumita distanta fata de oameni.\n\n"

    if (distanta_sprancene - 23) == 0:
        text = text + "Persoana este foarte sensibila de critici, se supara repede si traiesc cu impresia ca cineva le doreste raul.\nIn general, se vad navoiti sa depuna un efort dublu pentru a obtine acelasi succes precum o persoana care nu are sprancenele unite. De asemenea, sunt introvertiti si timizi.\n\n"
    else:
        if distanta_sprancene - 23 > distanta_intre_ochi:
            text = text + "Peroana este intelegatoare, rabdatoare si are inima plina de compasiune.\nSe face cu usurinta iubita si acceptata de cei din jurul ei deoarece are un caracter placut. E generoasa, loiala si un foarte bun prieten.\n\n"
        else:
            text = text + "Persoana are o putere foarte mare de concentrare, atentie la detalii, precisa si da dovada de acuratete.\nCel mai bine pentru ea ese sa aiba mai multe independenta la locul de munca sau sa inceapa o afacer pe cont propriu.\n\n"

    if int(dicti['pupil_right'].x) < int(dicti['mouth_right'].x + 10):
        text = text + "Persoana este introvertita, centrata pe ea insasi, su o vointa puternuca si sceptica, nu se imprieteneste usor cu oricine, e practica,\ncumpatata mental si lupta cu hotarare pentru succes ori pentru a-si atinge scopul. Critica lumea si detesta falsitatea.\n\n"
    else: text = text + "Persoana este curajoasa, energica, are nevoie sa fie in centrul atentiei si este lipsita de timiditatee. Poate ajunge un om influent sau afacerist de succes.\nInspira incredere si iubeste sa traiasca viata intens. Rade mult, socializeaza cu placere si se imprietenesc usor.\n\n"

    # print(lungimea_gurii)
    # print(marimea_nas*(-3)+40)
    if (marimea_nas*(-3) + 40) > lungimea_gurii:
        text = text + "Persoana are o parere buna desprea ea insasi si este independenta, este foarte ambitioasa, ii place sa actioneze dupa bunul plac si este un lider bun.\n\n"
    else: text = text + "Persoana are putin incredere in ea insasi, evita activitatile care presupun pozitii sociale inalte si opteaza pentru cele care presupun munca in echipa.\n\n"

    return text

    # dicti1 = {
    #     'distanta_intre_pupile' : distanta_intre_pupile,
    #     'aria' : arie,
    #     'marimea_ochi_latura_a' : marimea_ochi_latura_a,
    #     'marimea_ochi_latura_b': marimea_ochi_latura_b,
    #     'lungimea_gurii' : lungimea_gurii,
    #     'lungimea_sprancenelor_stanga': lungimea_sprancenelor_stanga,
    #     'lungimea_sprancenelor_dreapta' : lungimea_sprancenelor_dreapta
    # }
    # return dicti, dicti1