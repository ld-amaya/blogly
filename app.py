from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from users import Users

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iamlou'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route("/")
def homepage():
    """Returns the home page"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("/posts/home.html", posts=posts)

######## USERS GET REQUESTS #######################################


@app.route("/users")
def show_all_users():
    """ Shows all users """
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/new")
def add_new_user():
    """Shows the add new user form"""
    return render_template("new_user.html")


@app.route("/users/<int:id>")
def get_user_details(id):
    """Returns user detaisl"""
    user = User.query.get_or_404(id)
    return render_template("user_details.html", user=user)


@app.route("/users/<int:id>/edit")
def edit_user_details(id):
    """Edit user details"""
    user = User.query.get_or_404(id)
    return render_template("user_edit.html", user=user)


######## POST GET REQUESTS #######################################

@app.route("/users/<int:id>/posts")
def get_user_posts():
    """Populate user detals and posts"""
    user = User.query.get_or_404(id)
    return render_template("user_posts.html", user=user)


@app.route("/users/<int:id>/posts/new")
def create_new_post(id):
    """Creates a new post for user"""
    user = User.query.get_or_404(id)
    return render_template("posts/new.html", user=user)


@app.route("/posts/<int:post_id>")
def get_post(post_id):
    """Retrieves the post"""
    post = Post.query.get_or_404(post_id)
    return render_template("posts/show.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Retrieves the post"""
    post = Post.query.get_or_404(post_id)
    return render_template("posts/edit.html", post=post)


########### CREATE  ROUTES ############################


@app.route("/users/new", methods=["POST"])
def add_user_to_db():
    """Add the user to the database"""
    user = Users(request.form['first_name'],
                 request.form['last_name'],
                 request.form['image_url']
                 )
    user.add_user()
    return redirect("/users")


@app.route("/users/<int:id>/posts/new", methods=["POST"])
def add_new_post(id):
    """Add new post to database"""
    post = Post(title=request.form['title'],
                content=request.form['content'],
                user_id=id)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{id}")


########### EDIT ROUTES ############################


@app.route("/users/<int:id>/edit", methods=["POST"])
def update_user_to_db(id):
    """Update user details to the database"""
    # Get existing user data
    user = Users(request.form['first_name'],
                 request.form['last_name'],
                 request.form['image_url']
                 )
    user.update_user(id)
    flash(
        f"Successfully udpated profile", "updated")
    return redirect(f"/users/{id}")


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Updates post on the database"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    flash(
        f"Successfully udpated the post {post.title}", "updated")
    return redirect(f"/posts/{post.id}")


########### DELETE ROUTES ############################

@app.route("/users/<int:id>/delete", methods=["POST"])
def delete_user(id):
    """Deletes user from the database"""
    user = User.query.get_or_404(id)
    username = user.first_name
    db.session.delete(user)
    db.session.commit()
    flash(
        f"Successfully deleted {username} user", "deleted")
    return redirect("/users")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Deletes post from the database"""
    post = Post.query.get_or_404(post_id)
    title = post.title
    by = post.user.first_name
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    flash(
        f"Successfully deleted the post {title}", "deleted")
    return redirect(f"/users/{user_id}")
