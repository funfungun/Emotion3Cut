import os

# 표정인식 디렉토리 안의 모든 파일 삭제
directory = r"temp"
files = os.listdir(directory)
for file in files:
    file_path = os.path.join(directory, file)
    os.remove(file_path)