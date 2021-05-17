from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bloglydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'development_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/', methods=['POST'])
def create_new_user():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    new_user = User(first_name = firstname, last_name = lastname)
    db.session.add(new_user)
    db.session.commit()
    flash('User created successfully!')
    return redirect('/')