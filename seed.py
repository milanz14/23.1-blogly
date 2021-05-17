from models import User, db
from app import app

#create all tables and seed the data
db.drop_all()
db.create_all()

u1 = User(first_name='User1', last_name='User1 Last')
u2 = User(first_name='User2', last_name='User2 Last')

db.session.add(u1)
db.session.add(u2)
db.session.commit()
