
from dotenv import load_dotenv
from fastapi import FastAPI, Request

load_dotenv()

from src.graph.workflow import build_workflow

app = FastAPI()


@app.post("/ask")
async def ask(request: Request):
    query = (await request.body()).decode("utf-8")
    workflow = build_workflow()
    result = workflow.invoke({"query": query})
    return {
        "departamento": result["departamento"],
        "razon": result["razon"],
        "respuesta": result["respuesta"],
    }


BOOKS = [
    {'title': 'Batman: Year One',        'author': 'Frank Miller', 'category': 'superhero'},
    {'title': 'The Dark Knight Returns', 'author': 'Frank Miller', 'category': 'superhero'},
    {'title': 'Watchmen',                'author': 'Alan Moore',   'category': 'graphic-novel'},
    {'title': 'The Killing Joke',        'author': 'Alan Moore',   'category': 'graphic-novel'},
    {'title': 'Green Lantern: Rebirth',  'author': 'Geoff Johns',  'category': 'superhero'},
    {'title': 'Superman: Red Son',       'author': 'Mark Millar',  'category': 'graphic-novel'},
]


@app.get("/books")
async def read_all_books():
    return BOOKS

