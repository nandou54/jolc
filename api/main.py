from os import path
from pydantic import BaseModel
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse
from starlette.exceptions import HTTPException

from interpreter.main import interpret
from translator.main import translate
from optimizer.eyehole import optimize as optimize_eyehole
from optimizer.blocks import optimize as optimize_blocks


class InputData(BaseModel):
  content: str

mime_types = {
  'txt':'text/plain',
  'js':'text/javascript',
  'css':'text/css',
  'jpg':'image/jpeg',
  'jpeg':'image/jpeg',
  'png':'image/png',
  'svg':'image/svg+xml'
}


app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_credentials = True,
  allow_headers = ['*'],
  allow_methods = ['POST'],
  allow_origins = ['http://localhost:3000']
)

@app.get('/')
async def redirect_base():
  return RedirectResponse('/jolc/')

router = APIRouter(prefix = '/jolc')

@router.post('/api/interpret')
def analyze_input(input_data: InputData):
  return interpret(input_data.content)

@router.post('/api/translate')
def analyze_input(input_data: InputData):
  return translate(input_data.content)

@router.post('/api/optimize/eyehole')
def analyze_input(input_data: InputData):
  return optimize_eyehole(input_data.content)

@router.post('/api/optimize/blocks')
def analyze_input(input_data: InputData):
  return optimize_blocks(input_data.content)

@router.get('/')
async def read_index():
    return FileResponse('dist/index.html')

@router.get('/{filename:path}')
async def serve_file(request: Request, filename):
  file_path = 'dist/' + filename

  if not path.exists(file_path):
    return FileResponse('dist/index.html')

  file_array = filename.split('.')

  extension = file_array[-1].lower() if len(file_array)>1 else 'txt'
  if extension not in mime_types.keys():
    extension = 'txt'

  return FileResponse(file_path, media_type=mime_types[extension])


app.include_router(router)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
  return RedirectResponse('/')
