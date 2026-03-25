
from fastapi import Body, FastAPI

app = FastAPI()


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

