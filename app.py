import uvicorn
import logging
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.file_utils import is_allowed_file, ALLOW_MAX_FILE_SIZE, get_uniq_file_name


#дописать проверку существования директории и добавить запрет удаления директории
logs_dir = Path("logs")
log_file = logs_dir / "app.log"
#добавить кучу логирования на try-except при проверке всяких типов и т.п.
logging.basicConfig(
    level=logging.ERROR,
    format="[{asctime}] - {levelname} - {message}",
    style="{",
    handlers=[
        logging.FileHandler(log_file, mode="a", encoding="utf-8"),
        logging.StreamHandler(),
    ]
)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})

@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
    return templates.TemplateResponse("upload.html", {'request': request})

@app.post("/upload/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    # тут нужно добавить доп проверки размера

    print('Файл загружен', file.filename)
    my_file = Path(file.filename)
    if is_allowed_file(my_file):
        print('Верное расширение')

    else:
        logging.error('Wrong file type error')
        print('Неверное расширение')




    # return templates.TemplateResponse("upload.html", {'request': request, 'file': file})
    # return PlainTextResponse(f'Файл отправлен')
    content = await file.read(ALLOW_MAX_FILE_SIZE + 1)

    #здесь нужно сделать наоборот и добавить исключения

    if len(content) < ALLOW_MAX_FILE_SIZE:
        print(f'Size OK {len(content)}')
        new_file_name = get_uniq_file_name(my_file)
        print(f'New file name: {new_file_name}')

        image_dir = Path("images")
        image_dir.mkdir(exist_ok=True) # создаем папку, если ее нет
        save_path = image_dir / new_file_name

        save_path.write_bytes(content)
        print(f'Файл {str(save_path)} записан')

        return {'message': f'Файл {file.filename} загружен\nСохранен в {save_path}'}
    else:
        print(f'Size NOT OK {len(content)}, allowed {ALLOW_MAX_FILE_SIZE}')

@app.get("/images/", response_class=HTMLResponse)
async def images(request: Request):
    return templates.TemplateResponse("images.html", {'request': request})

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000)


    # CREATE TABLE images (
    #     id SERIAL PRIMARY KEY,
    #     filename TEXT NOT NULL,
    #     original_name TEXT NOT NULL,
    #     size INTEGER NOT NULL,
    #     upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #     file_type TEXT NOT NULL
    # );