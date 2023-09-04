from libs.FacialExpression import DataAnalyzer
from libs.Face import FacialLandmarkDetector
from libs.FacialExpression import FacialExpressionRecognizer
import cv2
import numpy as np
import os
import libs.Face as Face


def main():
    facial_landmark_detector = FacialLandmarkDetector(
        model=Face.FACIAL_LANDMARK_DETECTION_MODEL_MEDIAPIPE,
        face_detector=Face.FACE_DETECTION_MODEL_OPENCV_DNN)

    cap = cv2.VideoCapture(0)

    while True:

        _, frame = cap.read()

        frame = cv2.flip(frame, 1)

        facial_landmark_detector.feed(frame)

        if facial_landmark_detector.getIsDetect():

            face = facial_landmark_detector.getFace()

            cv2.rectangle(frame, (face.getX(), face.getY()), (face.getX()+face.getW(), face.getY()+face.getH()), (0, 255, 0), 3)


        cv2.imshow("frame", frame)

        key = cv2.waitKey(1)

        if key == 27:
            break

    cap.release()


if __name__ == '__main__':
    main()