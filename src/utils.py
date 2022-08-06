from flask import Request
from flask_sqlalchemy import SQLAlchemy
from loguru import logger
import requests

from src.models import Question


def validate(req: Request):
    num = req.json.get("questions_num")
    if num is None:
        raise KeyError("You need to send JSON with 'questions_num' key")
    if not isinstance(num, int):
        raise ValueError("'questions_num' should be integer")
    return num


def get_last_previous_question(database: SQLAlchemy):
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
                    "created_at": res.created_at,
                }
            )
        database.session.commit()
    except Exception:
        database.session.rollback()
        raise
    return results


def get_response_from_api(api_url: str, count: int):
    api_response = requests.get(api_url + f"{count}")

    questions = []
    for response in api_response.json():
        while Question.query.filter_by(id=response["id"]).all():
            logger.debug("Same question! Retrying.")
            response = requests.get(api_url + "1").json()[0]

        question = Question(
            id=response["id"],
            question=response["question"],
            answer=response["answer"],
            created_at=response["created_at"],
            last_request=True,
        )
        questions.append(question)
    return questions


def save_to_db(questions: list[Question], database: SQLAlchemy):
    try:
        for question in questions:
            database.session.add(question)
        database.session.commit()
    except Exception:
        database.session.rollback()
        raise
