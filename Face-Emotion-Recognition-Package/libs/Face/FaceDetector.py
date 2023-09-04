import cv2
import os
import numpy as np

FACE_DETECTION_MODEL_DLIB = 0
FACE_DETECTION_MODEL_OPENCV_DNN = 1
FACE_DETECTION_MODEL_SFD = -1  # 아직 구현 안됨

DNN_proto_path = os.path.abspath("assets/deploy.prototxt")
DNN_model_path = os.path.abspath("assets/res10_300x300_ssd_iter_140000.caffemodel")


class FaceDetector:
    def __init__(self, model=FACE_DETECTION_MODEL_DLIB):
        self.__detector__ = None
        self.__model_name__ = model
        self.__is_detect__ = False
        self.__face_roi__ = None

        if model == FACE_DETECTION_MODEL_DLIB:
            import dlib
            self.__detector__ = dlib.get_frontal_face_detector()
            pass

        elif model == FACE_DETECTION_MODEL_OPENCV_DNN:
            self.__detector__ = cv2.dnn.readNetFromCaffe(DNN_proto_path, DNN_model_path)

        elif model == FACE_DETECTION_MODEL_SFD:
            self.__is_detect__ = True
            self.__face_roi__ = None
            pass

        else:
            print("No Face Detection model")
            return

    def feed(self, img):

        if self.__detector__ == None:
            print("Please initialize Face Detection Model")
            return

        if self.__model_name__ == FACE_DETECTION_MODEL_DLIB:
            self.face_detection_dlib(img)

        elif self.__model_name__ == FACE_DETECTION_MODEL_OPENCV_DNN:
            self.face_detection_opencv(img)

    def face_detection_dlib(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = self.__detector__(gray)

        if len(faces) > 0:
            self.__is_detect__ = True
            for face in faces:
                x = face.left()
                y = face.top()
                w = face.right() - face.left()
                h = face.bottom() - face.top()

                self.__face_roi__ = Face(x=x, y=y, w=w, h=h)

        elif len(faces) == 0:
            self.__is_detect__ = False
            self.__face_roi__ = None

    def face_detection_opencv(self, img, threshold=0.5):
        """
        Get the bounding box of faces in image using dnn.
        """
        rows, cols, _ = img.shape

        confidences = []
        faceboxes = []
        # cv2.dnn.blobFromImage()
        self.__detector__.setInput(cv2.dnn.blobFromImage(img, 1.0, (150, 150), (104.0, 177.0, 123.0), False, False))
        detections = self.__detector__.forward()

        # print(detections.shape)
        for result in detections[0, 0, :, :]:  # 200, 7
            confidence = result[2]
            # 200개의 결과들 중 threshold를 넘긴 값들만 계산 후 append
            if confidence > threshold:
                x_left_top = int(result[3] * cols)  # left : 왼쪽 위 x
                y_left_top = int(result[4] * rows)  # top : 왼쪽 위 y
                x_right_bottom = int(result[5] * cols)  # right : 오른쪽 아래 x
                y_right_bottom = int(result[6] * rows)  # bottom : 오른쪽 아래 y
                confidences.append(confidence)  # confidence 저장
                faceboxes.append(
                    [x_left_top, y_left_top, x_right_bottom, y_right_bottom])  # [ left, top, right, bottom]

        if len(faceboxes) > 0:
            self.__is_detect__ = True

            box = [faceboxes[0][0], faceboxes[0][1], faceboxes[0][2], faceboxes[0][3]]

            box = self.make_square_box(box)

            x = box[0]
            y = box[1]
            w = box[2] - box[0]
            h = box[3] - box[1]

            print(x)

            self.__face_roi__ = Face(x=x, y=y, w=w, h=h)

        else:
            self.__is_detect__ = False
            self. __face_roi__ = None

        # self.detection_result = [faceboxes, confidences]
        #
        # return confidences, faceboxes

    def make_square_box(self, box):
        left = int(box[0])
        top = int(box[1])
        right = int(box[2])
        bottom = int(box[3])

        diff_height_width = (bottom - top) - (right - left)
        offset_y = int(abs(diff_height_width / 2))

        if diff_height_width > 0:
            left -= offset_y
            right += offset_y

        elif diff_height_width < 0:
            top -= offset_y
            bottom += offset_y

        width = right - left
        height = bottom - top

        diff = height - width
        delta = int(abs(diff) / 2)

        if diff == 0:  # Already a square.
            return [left, top, right, bottom]
        elif diff > 0:  # Height > width, a slim box.
            left -= delta
            right += delta
            if diff % 2 == 1:
                right += 1
        else:  # Width > height, a short box.
            top -= delta
            bottom += delta
            if diff % 2 == 1:
                bottom += 1

        # Make sure box is always square.
        test_w = right - left
        test_h = bottom - top
        assert ((right - left) == (bottom - top)), 'Box is not square.'

        return [left, top, right, bottom]


    def getFace(self):
        return self.__face_roi__

    def getIsDetect(self):
        return self.__is_detect__


class Face:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getW(self):
        return self.w

    def getH(self):
        return self.h




