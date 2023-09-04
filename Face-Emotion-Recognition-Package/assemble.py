import os
from PIL import Image

# 이전 표정인식 디렉토리 안의 모든 파일 삭제
directory = r"temp"
files = os.listdir(directory)
for file in files:
    file_path = os.path.join(directory, file)
    os.remove(file_path)

# 이미지 목록
imagePaths = ["pic\\1.png",
              "pic\\2.png",
              "pic\\3.png",
              "template.png"]

# 출력 이미지의 경로
outputPath = "gamsung.png"

# 결과 이미지 크기 가져오기
newWidth = 0
newHeight = 0
for imagePath in imagePaths:
    with Image.open(imagePath) as image:
        size = image.size
        newWidth = max(newWidth, size[0])
        newHeight += size[1]

# 이미지를 새 이미지로 결합
newImage = Image.new("RGB", (newWidth, newHeight))

stitchedHeight = 0
for imagePath in imagePaths:
    with Image.open(imagePath) as image:
        newImage.paste(image, (0, stitchedHeight))
        stitchedHeight += image.size[1]

# 결과 이미지 저장
newImage.save(outputPath)

# 결과 이미지 띄우기
newImage.show()

# 디렉토리 안의 모든 파일 삭제
directory = r"pic"
files = os.listdir(directory)
for file in files:
    file_path = os.path.join(directory, file)
    os.remove(file_path)