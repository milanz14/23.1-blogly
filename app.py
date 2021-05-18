from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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

@app.route('/users/new')
def show_add_form():
    """ show the add form for a new user """
    return render_template('newuser.html')

@app.route('/users/new', methods=['POST'])
def create_new_user():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    new_user = User(first_name = firstname, last_name = lastname)
    db.session.add(new_user)
    db.session.commit()
    flash('User created successfully!')
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """ show details for a specific user """
    foundUser = User.query.get_or_404(user_id)
    foundUserPosts = Post.query.filter(Post.user_id==user_id)
    return render_template('userdetails.html', foundUser=foundUser,foundUserPosts=foundUserPosts)

@app.route('/users/<int:user_id>/edit', methods=['GET','POST'])
def edit_user(user_id):
    """ edit details for specific user """
    foundUser = User.query.get_or_404(user_id)
    if request.method == 'POST':
        foundUser.first_name = request.form['firstname']
        foundUser.last_name = request.form['lastname']
        db.session.commit()
        flash('User details updated!')
        return redirect('/users')
    else:
        return render_template('edituserform.html', foundUser=foundUser)

@app.route('/users/<int:user_id>/delete', methods=['GET','POST'])
def delete_user(user_id):
    """ delete a particular user """
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    flash('User Deleted!')
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """ show the form for a specific user's new posts """
    foundUser = User.query.get_or_404(user_id)
    return render_template('newpost.html', foundUser=foundUser)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_new_post(user_id):
    """ support adding a new post """
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    flash('Posted')
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_posts():
    """ show list of posts """
    pass

@app.route('/posts/<int:post_id>/edit', methods=['GET','POST'])
def show_posts_or_edit(post_id):
    """ show the posts and render a post edit form, redirect
    back to post view after updating a post """
    pass

@app.route('/posts/<int:post_id>/delete', methods=['GET','POST'])
def delete_post(post_id):
    """ delete a specific post """
    pass



