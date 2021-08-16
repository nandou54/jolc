from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from grammar import parser

class inputData(BaseModel):
  text: str

class outputData(BaseModel):
  output: list[str]


app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post("/api/")
def analyze_input(input: inputData):
  parser.parse(input.text)
  return input.text
