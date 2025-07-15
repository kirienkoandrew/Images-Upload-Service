from pathlib import Path
import uuid


ALLOW_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']
ALLOW_MAX_FILE_SIZE = 1024 * 1024 * 10


def is_allowed_file(filename: Path) -> bool:
    """Функция проверяет, есть ли расширение в списке разрешенных"""
    #ext = filename.rsplit('.', maxsplit=1)[-1]
    ext = filename.suffix.lower()[1:]
    # print(ext)
    return ext in ALLOW_EXTENSIONS


def get_uniq_file_name(filename: Path) -> str:
    """Функция генератор уникального имени файла"""
    ext = filename.suffix.lower()[1:]
    uniq_name = f'{uuid.uuid4().hex}.{ext}'
    print(uniq_name)
    return uniq_name



