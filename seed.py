from models import User, db
from app import app

#create all tables and seed the data
db.drop_all()
db.create_all()

u1 = User(first_name='Ron', last_name='Swanson')
u2 = User(first_name='Tom', last_name='Haverford')

db.session.add(u1)
db.session.add(u2)
db.session.commit()
