from flask import request, jsonify
from loguru import logger

from src import app, db
from src.utils import (
    get_last_previous_question,
    get_response_from_api,
    save_to_db,
    validate,
)


API_URL = "https://jservice.io/api/random?count="


@app.post("/questions")
def process():
    try:
        num = validate(request)
    except KeyError as err:
        logger.warning(err)
        return str(err), 400
    except ValueError as err:
        logger.warning(err)
        return str(err), 400

    try:
        response_payload = get_last_previous_question(db)
        questions = get_response_from_api(API_URL, num)
        save_to_db(questions, db)

    except Exception as err:
        logger.exception(err)
        return str(err), 500

    return jsonify(response_payload), 200
