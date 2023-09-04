from PyQt5.QtWidgets import *
import os
import sys
import cv2 as cv

class Video(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('표정 인식')  # 윈도우 이름과 위치 지정
        self.setGeometry(200, 200, 300, 100)

        videoButton = QPushButton('카메라 켜기', self)  # 버튼 생성
        captureButton = QPushButton('촬영', self)

        videoButton.setGeometry(10, 10, 100, 30)  # 버튼 위치와 크기 지정
        captureButton.setGeometry(110, 10, 100, 30)

        videoButton.clicked.connect(self.videoFunction)  # 콜백 함수 지정
        captureButton.clicked.connect(self.captureFunction)

    def videoFunction(self):
        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)  # 카메라와 연결 시도
        if not self.cap.isOpened(): self.close()

        while True:
            ret, self.frame = self.cap.read()
            if not ret: break

            self.frame = cv.flip(self.frame, 1)
            cv.imshow('video display', self.frame)
            cv.waitKey(1)

    def captureFunction(self):
        self.capturedFrame = self.frame
        self.cap.release()
        self.close()

        directory = r"temp"
        filename = "check.png"
        filepath = os.path.join(directory, filename)
        cv.imwrite(filepath, self.capturedFrame)

app = QApplication(sys.argv)
win = Video()
win.show()
app.exec_()