import os
from pydantic import BaseModel
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.exceptions import HTTPException

from interpreter import interpret

class inputData(BaseModel):
  text: str

class outputData(BaseModel):
  output: list[str]


app = FastAPI()

# origins = ["http://127.0.0.1:8000"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

mime_types = {
  'js':'text/javascript',
  'css':'text/css',
  'jpg':'image/jpeg',
  'png':'image/png',
  'svg':'image/svg+xml',
  'txt':'text/plain'
}

templates = Jinja2Templates(directory="../dist")

@app.post("/api/")
def analyze_input(input: inputData):
  result = interpret(input.text)
  return result

@app.get("/client")
async def serve_app(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

@app.get("/client/static/{filename}")
async def serve_file(request: Request, filename):
  file_path ='../dist/static/'+filename

  if not os.path.exists(file_path):
    return {"error":"File not found"}

  file_array = filename.split('.')

  extension = 'txt'
  if len(file_array)>1:
    extension = file_array[-1].lower()

  if extension not in mime_types.keys():
    extension = 'txt'

  return FileResponse(file_path, media_type=mime_types[extension])

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return RedirectResponse("/client")
