from PyQt5.QtWidgets import *
import os
import sys
import cv2 as cv
from pixellib.tune_bg import alter_bg

# 이전 표정인식 디렉토리 안의 모든 파일 삭제
directory = r"temp"
files = os.listdir(directory)
for file in files:
    file_path = os.path.join(directory, file)
    os.remove(file_path)

class Video(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('슬픔')  # 윈도우 이름과 위치 지정
        self.setGeometry(200, 200, 500, 100)

        videoButton = QPushButton('카메라 켜기', self)  # 버튼 생성
        captureButton = QPushButton('촬영', self)
        self.pickCombo = QComboBox(self)
        self.pickCombo.addItems(['원본', '회색', '검정색'])
        saveButton = QPushButton('저장', self)

        videoButton.setGeometry(10, 10, 100, 30)  # 버튼 위치와 크기 지정
        captureButton.setGeometry(110, 10, 100, 30)
        self.pickCombo.setGeometry(210, 10, 100, 30)
        saveButton.setGeometry(310, 10, 100, 30)

        videoButton.clicked.connect(self.videoFunction)  # 콜백 함수 지정
        captureButton.clicked.connect(self.captureFunction)
        self.pickCombo.currentIndexChanged.connect(self.selectFunction)
        saveButton.clicked.connect(self.saveFunction)

    def videoFunction(self):
        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)  # 카메라와 연결 시도
        if not self.cap.isOpened(): self.close()

        while True:
            ret, self.frame = self.cap.read()
            if not ret: break
            cv.imshow('video display', self.frame)
            cv.waitKey(1)

    def captureFunction(self):
        self.capturedFrame = self.frame
        self.original = self.capturedFrame
        cv.imshow('Captured Frame', self.capturedFrame)
        self.cap.release()
        cv.destroyWindow('video display')
        self.check = True

        directory = r"temp"
        filename = "check2.png"
        filepath = os.path.join(directory, filename)
        cv.imwrite(filepath, self.capturedFrame)

    def selectFunction(self):
        pick_effect = self.pickCombo.currentIndex()
        if (self.check == True):
            cv.destroyWindow('Captured Frame')
            self.check = False

        if pick_effect == 0:
            self.capturedFrame = self.original
        elif pick_effect == 1:  # 회색
            self.capturedFrame = change_bg.change_bg_img(f_image_path="temp/check2.png", b_image_path=
            "frame/sad1.png", detect="person")
        elif pick_effect == 2:  # 검정색
            self.capturedFrame = change_bg.change_bg_img(f_image_path="temp/check2.png", b_image_path=
            "frame/sad2.png", detect="person")
        cv.imshow('show', self.capturedFrame)

    def saveFunction(self):  # 파일 저장
        directory = r"pic"
        filename = "1.png"
        filepath = os.path.join(directory, filename)

        count = 1
        while os.path.exists(filepath):
            count += 1
            filename = f"{count}.png"
            filepath = os.path.join(directory, filename)

        cv.imwrite(filepath, self.capturedFrame)
        self.close()

change_bg = alter_bg(model_type="pb")
change_bg.load_pascalvoc_model('xception_pascalvoc.pb')

app = QApplication(sys.argv)
win = Video()
win.show()
app.exec_()