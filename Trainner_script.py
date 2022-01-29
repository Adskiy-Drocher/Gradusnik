import cv2

import os
import numpy as np
from PIL import Image


class Trainer(object):
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.dir_path = ''
        self.faceSamples = []
        self.Ids = []

    def getImagesAndLabels(self, path):
        self.dir_path = path
        for el in os.listdir(self.dir_path):
            if (os.path.split(el)[-1].split(".")[-1] != 'jpg'):
                continue
            pilImage = Image.open(self.dir_path + '/' + el).convert('L')
            imageNp = np.array(pilImage, 'uint8')
            Id = int(os.path.split(el)[-1].split(".")[1])
            #print(f'Ойдишнег {Id}')
            faces = self.detector.detectMultiScale(imageNp)
            for (x, y, w, h) in faces:
                self.faceSamples.append(imageNp[y:y + h, x:x + w])
                self.Ids.append(Id)
        #print(f'ID: {self.Ids}')
        #print(f'Список {self.faceSamples}')
        self.recognize()

    def recognize(self):
        self.recognizer.train(self.faceSamples, np.array(self.Ids))
        self.recognizer.save(self.dir_path + '/' + 'trainner.yml')
        print('Путь к дириктории', self.dir_path)

