from db_instance import db


class User(db.Model):

    __tablename__ = 't_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    gender = db.Column(db.Boolean, default=True)

    def __repr__(self):

        return f"<User {self.username}>"
