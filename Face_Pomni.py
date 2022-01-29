import cv2
import os



class Image_maker():
    def __init__(self):
        self.vid_cam = cv2.VideoCapture(0)
        self.vid_cam.set(3, 640)  # ширина кадра
        self.vid_cam.set(4, 480)
        self.face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.user_id = 0
        self.count = 0
        self.direct_path = ''
        self.img = cv2.imread('yeba.jpg', cv2.IMREAD_COLOR)
        self.path = ''

    def make_dir(self, user_id, path):
        user_id = str(user_id)
        print('Путь к чему-то', path)
        os.mkdir(rf'{path}/{user_id}')
        return f'{path}/{user_id}'




    def take_image(self, user_id, path):
        self.user_id = user_id
        self.path = path
        path_dir = self.make_dir(user_id=self.user_id, path=self.path)
        print(path_dir)
        while True:
            grey = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
            for (x, y, w, h) in faces:
                cv2.rectangle(self.img, (x, y), (x + w, y + h), 255, 0, 0, 2)
                roi_gray = grey[y:y + h, x:x + w]
                roi_color = self.img[y:y + h, x:x + w]
                self.count += 1
                cv2.imwrite(path_dir + '/' + str(self.user_id) + "." + str(self.count) + ".jpg", grey[y:y + h, x:x + w])
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif self.count > 99:
                break
        #print("\ n [INFO] Выход из программы и очистка")
        # Остановить видео
        #self.vid_cam.relea8se()
        # Закройте все запущенные окна
        cv2.destroyAllWindows()

