from SQLite import engine, metadata, session, User
import cv2
import numpy as np



class Recognizer(object):
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.cascadePath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.names = dict()
        self.yml_path = ''
        for x in range(len(session.query(User.name, User.id).all())):
            list = session.query(User.name, User.id).all()[x]
            self.names[str(list[1])] = list[0]
            y = session.query(User.id)[x]
            #print('Имена' ,self.names)


    def start(self, yml_path, ID):
        self.yml_path = yml_path
        self.recognizer.read(yml_path)
        name = self.names[ID]
        cam = cv2.VideoCapture(0)
        cam.set(3,640)
        cam.set(4,480)
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces=self.faceCascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (int(minW), int(minH)))
        for(x,y,w,h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            Id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
            if (confidence) < 100:
                confidence = "  {0}%".format(round(100 - confidence))
                #print(f'{confidence}%')
            else:
                confidence = "  {0}%".format(round(100 - confidence))

                #print(f'{confidence}%')
        print(f'Путь: {yml_path}, Имя: {name}, Вероятность: {confidence}')




        cam.release()
        cv2.destroyAllWindows()