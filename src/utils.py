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

    last_question: Question = Question.query.filter_by(last_request=True).one_or_none()

    if last_question is None:
        return None

    try:
        last_question.last_request = False
        result = {
            "id": last_question.id,
            "question": last_question.question,
            "answer": last_question.answer,
            "created_at": last_question.created_at,
        }
        database.session.commit()
    except Exception:
        database.session.rollback()
        raise
    return result


def get_response_from_api(api_url: str, count: int):
    api_response = requests.get(api_url + f"{count}")

    response_objects = list(api_response.json())

    questions = []
    for index, response in enumerate(response_objects):
        while Question.query.filter_by(id=response["id"]).one_or_none():
            logger.debug("Same question! Retrying.")
            response = requests.get(api_url + "1").json()[0]

        if index < (len(response_objects) - 1):
            question = Question(
                id=response["id"],
                question=response["question"],
                answer=response["answer"],
                created_at=response["created_at"],
                last_request=False,
            )
        else:
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
