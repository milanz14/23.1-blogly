from flask_sqlalchemy import SQLAlchemy

# initialize SQLA and set up the server
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# Model for User

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, default='https://images.unsplash.com/photo-1586314265219-192da32be7eb?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80')

