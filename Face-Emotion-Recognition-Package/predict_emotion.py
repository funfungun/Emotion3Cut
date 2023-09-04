from libs.Face import FacialLandmarkDetector
import libs.Face as Face
import cv2
import numpy as np
import joblib
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# 저장된 모델 로드
model_path = "mlp_model_3.pkl"
model = joblib.load(model_path)

# 새로운 이미지를 로드하고 전처리합니다.
new_image_path = "temp\\check.png"
new_img = cv2.imread(new_image_path)
new_img = cv2.resize(new_img, (480, 640))

# 얼굴 특징점 검출 모듈 선언
facial_landmark_detector = FacialLandmarkDetector(
        model=Face.FACIAL_LANDMARK_DETECTION_MODEL_MEDIAPIPE,
        face_detector=Face.FACE_DETECTION_MODEL_OPENCV_DNN)

def min_max_normalization(value):
    value = list(value)

    _max = max(value)
    _min = min(value)

    result = []

    for val in value:
        _val = (val - _min) / (_max - _min)
        result.append(_val)

    return np.array(result)


# 감정 레이블 정의 happiness = 0, sadness = 1, anger = 2
emotion_labels = ['happiness', 'sadness', 'angry']

# 얼굴 특징점 검출을 수행합니다.
facial_landmark_detector.feed(new_img)
if facial_landmark_detector.getIsDetect():
    landmarks = facial_landmark_detector.getFacialLandmark()
    x = landmarks.getX()
    y = landmarks.getY()

    # 얼굴 특징점을 정규화합니다.
    normalized_landmark_x = min_max_normalization(x)
    normalized_landmark_y = min_max_normalization(y)

    # 특징 벡터를 생성합니다.
    new_feature_vector = np.concatenate((normalized_landmark_x, normalized_landmark_y))

    # 훈련된 모델을 사용하여 감정을 예측합니다.
    # predicted_emotion = model.predict(new_feature_vector.reshape(1, -1))
    # predicted_emotion_label = emotion_labels[predicted_emotion]
    # print("예측된 감정:", predicted_emotion_label)
    predicted_emotion = model.predict(new_feature_vector.reshape(1, -1))
    predicted_emotion_label = emotion_labels[predicted_emotion[0]]
    print("emotion:", predicted_emotion_label)

    directory = r"temp"
    new_filename = f"{predicted_emotion_label}.png"
    new_filepath = os.path.join(directory, new_filename)

    # 파일 이름 변경
    os.rename(new_image_path, new_filepath)

else:
    print("이미지에서 얼굴을 찾을 수 없습니다.")