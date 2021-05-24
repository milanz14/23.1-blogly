from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag

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
def show_posts(post_id):
    """ show list of posts """
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template('postdetails.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit', methods=['GET','POST'])
def show_posts_or_edit(post_id):
    """ show the posts and render a post edit form, redirect
    back to post view after updating a post """
    foundPost = Post.query.get_or_404(post_id)
    foundUser = User.query.get_or_404(foundPost.user_id)
    if request.method == 'POST':
        foundPost.title = request.form['title']
        foundPost.content = request.form['content']
        db.session.commit()
        flash('Post updated!')
        return redirect(f'/posts/{post_id}')
    else:
        return render_template('editpost.html', foundPost=foundPost, foundUser=foundUser)

@app.route('/posts/<int:post_id>/delete', methods=['GET','POST'])
def delete_post(post_id):
    """ delete a specific post """
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    flash('Post has been deleted!')
    return redirect('/users')

@app.route('/tags')
def display_all_tags():
    """ display all of the tags in the DB
    link to tag details page """
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """ display detail for a specific tag """
    foundTag = Tag.query.get_or_404(tag_id)
    # the filter_by method doesn't work here so get_or_404 fixes the issue
    # must be better to use get_or_404 as a general rule of thumb?
    return render_template('tagdetail.html', foundTag=foundTag)

@app.route('/tags/<int:tag_id>/edit', methods=['GET','POST'])
def edit_specific_tag(tag_id):
    """ display edit for for changing the name of a tag """
    foundTag = Tag.query.filter_by(id=tag_id)
    foundPosts = Post.query.all()
    if request.method == 'POST':
        foundTag.tag_name = request.form['tagname']
        db.session.commit()
        flash('Tag Updated!')
        return redirect(f'/tags/{tag_id}')
    else:
        return render_template('edittag.html', foundTag=foundTag, foundPosts=foundPosts)

# issue with the route above - not querying the TAG properly -- FIX

@app.route('/tags/new', methods=['GET','POST'])
def create_a_new_tag():
    """ render a form to create a new tag """
    if request.method == 'POST':
        new_tag_name = request.form['tagname']
        new_tag = Tag(tag_name=new_tag_name)
        db.session.add(new_tag)
        db.session.commit()
        flash('Success! New Tag Added!')
        return redirect('/tags')
    else:
        return render_template('newtag.html')

@app.route('/tags/<int:tag_id>/delete', methods=['GET','POST'])
def delete_specific_tag(tag_id):
    """ handle deletion of a tag """
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    flash('Tag has been deleted')
    return redirect('/tags')