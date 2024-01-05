import uvicorn

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from interpreter.main import interpret
from translator.main import translate
from optimizer.eyehole import optimize as optimize_eyehole
from optimizer.blocks import optimize as optimize_blocks


class InputData(BaseModel):
  content: str


app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_credentials = True,
  allow_headers = ['*'],
  allow_methods = ['POST'],
  allow_origins = ['http://localhost:3000', 'https://nanndo54.dev']
)

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
