from src import db


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    last_request = db.Column(db.Boolean)

    def __repr__(self):
        return f"<question:{self.id}, {self.created_at}>"
