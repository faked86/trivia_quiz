from flask import request

from src import app


@app.post('/questions')
def hello():
    return request.json
