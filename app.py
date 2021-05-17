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
def home():
    """ show the home page """
    return render_template('base.html')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users', methods=['POST'])
def create_new_user():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    new_user = User(first_name = firstname, last_name = lastname)
    db.session.add(new_user)
    db.session.commit()
    flash('User created successfully!')
    return redirect('/users')

@app.route('/users/new', methods=['GET','POST'])
def show_new_user_form():
    """ show new users add form"""
    pass

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """ show details for a specific user """
    foundUser = User.query.get_or_404(user_id)
    return render_template('userdetails.html', foundUser=foundUser)

@app.route('/users/<int:id>/edit', methods=['GET','POST'])
def edit_user(uid):
    """ edit details for specific user """
    pass

