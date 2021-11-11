from os import path
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.exceptions import HTTPException

from api.interpreter.main import interpret
from api.translator.main import translate
from api.optimizer.eyehole import optimize as optimize_eyehole
from api.optimizer.blocks import optimize as optimize_blocks

class InputData(BaseModel):
  content: str

app = FastAPI()

origins = [
  'http://localhost:3000'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_methods=['POST'],
  allow_credentials=True,
  allow_headers=['*']
)

mime_types = {
  'txt':'text/plain',
  'js':'text/javascript',
  'css':'text/css',
  'jpg':'image/jpeg',
  'jpeg':'image/jpeg',
  'png':'image/png',
  'svg':'image/svg+xml'
}

templates = Jinja2Templates(directory='dist')

@app.post('/api/interpret')
def analyze_input(input_data: InputData):
  return interpret(input_data.content)

@app.post('/api/translate')
def analyze_input(input_data: InputData):
  return translate(input_data.content)

@app.post('/api/optimize/eyehole')
def analyze_input(input_data: InputData):
  return optimize_eyehole(input_data.content)

@app.post('/api/optimize/blocks')
def analyze_input(input_data: InputData):
  return optimize_blocks(input_data.content)

@app.get('/static/{filename}')
async def serve_file(request: Request, filename):
  file_path ='dist/static/'+filename

  if not path.exists(file_path):
    return {'error': 'File not found'}

  file_array = filename.split('.')

  extension = file_array[-1].lower() if len(file_array)>1 else 'txt'
  if extension not in mime_types.keys():
    extension = 'txt'

  return FileResponse(file_path, media_type=mime_types[extension])

@app.get('/{rest_of_path:path}')
async def serve_app(request: Request, rest_of_path):
  return templates.TemplateResponse('index.html', {'request': request})

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
  return RedirectResponse('/')
