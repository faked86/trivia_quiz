from flask import request, jsonify
import requests

from src import app, db
from src.models import Question


API_URL = "https://jservice.io/api/random?count="


@app.post('/questions')
def process():
    num = request.json.get("questions_num")
    if num is None:
        return "You need to send JSON with 'questions_num' key", 400
    if not isinstance(num, int):
        return "'questions_num' should be integer", 400

    last_quest = Question.query.filter_by(last_request=True).all()
    results = []
    try:
        for res in last_quest:
            res.last_request = False
            results.append(
                {
                    "id": res.id,
                    "question": res.question,
                    "answer": res.answer,
                    "created_at": res.created_at
                }
            )
        db.session.commit()
    except Exception as err:
        print(err)
        db.session.rollback()

    api_response = requests.get(API_URL + f"{num}")
    try:
        for response in api_response.json():
            while Question.query.filter_by(id=response["id"]).all():
                print("Same question! Retrying.")
                response = requests.get(API_URL + "1").json()[0]

            question = Question(
                id=response["id"],
                question=response["question"],
                answer=response["answer"],
                created_at=response["created_at"],
                last_request=True,
            )
            db.session.add(question)
        db.session.commit()
    except Exception as err:
        print(err)
        db.session.rollback()

    return jsonify(results)
