import os
from PIL import Image
from fastapi import UploadFile

from error.exceptions import ImageProcessingError, WrongFileTypeError


def search_filename(file_id: str, dir_path: str):
    try:
        # 디렉토리 내의 파일들 검색
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            # 파일인지 확인
            if os.path.isfile(file_path):
                # 확장자 분리
                name, _ = os.path.splitext(filename)
                # 이름이 file_id와 일치하면 해당 파일 반환
                if name == file_id:
                    return file_path
    except Exception as e:
        return None


def get_image_path(file_id: str, search_in_dir: str):
    if file_id == None:
        return None

    # 파일이 저장된 디렉토리 경로
    file_id = file_id.split('.')[0] if '.' in file_id else file_id
    dir_path = search_in_dir

    # 디렉토리가 존재하지 않으면 기본 이미지 반환
    if not os.path.isdir(dir_path):
        return None

    return search_filename(file_id, dir_path)


def save_image(file_path: str, file: UploadFile, save_format: str = "JPEG"):
    if save_format not in ["JPEG", "PNG", "TIFF", "WEBP", "HEIF", "HEIC"]:
        raise ImageProcessingError("지원하지 않는 이미지 형식입니다.")

    # 파일 확장자를 file.filename에서 추출
    filename = file.filename
    if "." in filename:
        file_extension = filename.split(".")[-1].lower()
    else:
        raise WrongFileTypeError("파일 확장자를 찾을 수 없습니다.")

    # 이미지 파일 확장자만 허용 (jpg, jpeg, png, tiff, webp, heif, heic)
    allowed_extensions = ['jpg', 'jpeg',
                          'png', 'tiff', 'webp', 'heif', 'heic']
    if file_extension not in allowed_extensions:
        raise WrongFileTypeError("이미지만 받을 수 있습니다.")

    try:
        image = Image.open(file.file)
        rgb_image = image.convert("RGB")  # PNG, TIFF, HEIC 등은 RGB로 변환
        rgb_image.save(file_path, format="JPEG")
    except Exception as e:
        raise ImageProcessingError(f"이미지 처리 중 오류가 발생했습니다: {str(e)}")
