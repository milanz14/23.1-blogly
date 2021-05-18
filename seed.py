from models import User, Post, db
from app import app
from datetime import datetime

#create all tables and seed the data
db.drop_all()
db.create_all()

u1 = User(first_name='Ron', last_name='Swanson')
u2 = User(first_name='Tom', last_name='Haverford')
p1 = Post(title='First!', content='This is my first post!', created_at=datetime.now(), user_id=1)
p2 = Post(title='Second...!', content='My second post! Neato!', created_at=datetime.now(), user_id=1)

db.session.add(u1)
db.session.add(u2)
db.session.add(p1)
db.session.add(p2)
db.session.commit()
