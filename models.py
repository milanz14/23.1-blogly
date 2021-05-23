from flask_sqlalchemy import SQLAlchemy

# initialize SQLA and set up the server
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# Model for User

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, default='https://images.unsplash.com/photo-1586314265219-192da32be7eb?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80')

    posts = db.relationship('Post', backref='user')

    def __repr__(self):
        return f'<{self.first_name} {self.last_name}>'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
class PostTag(db.Model):
    __tablename__ = 'posttags'
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.Text, unique=True, nullable=False)

