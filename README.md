# TRIVIA_QUIZ

## INSTALLATION

Prerequisites:
- docker
- docker-compose
- git

Simply clone this repo:

```
git clone https://github.com/faked86/trivia_quiz.git
cd ip-telegram-bot
```

## USAGE

1. Run `docker-compose up` in terminal.


### API Server

- `POST localhost:8000/questions` - Send JSON in form like 
`{"questions_num": integer}` via Postman for example or
`curl -X POST -H "Content-Type: application/json"     -d '{"questions_num": 1}' localhost:8000/questions`


### Database

To connect to database I used PGadmin 4
- Login: pg
- Password: pass
- Database: quiz
- URL: localhost:5432