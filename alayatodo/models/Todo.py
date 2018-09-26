from alayatodo import db

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Integer, default=0)

    def __init__(self, user_id, description, completed=0):
        self.description = description
        self.user_id = user_id
        self.completed = completed

    def __repr__(self):
        return '<Todo %r>' % self.description