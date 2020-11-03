from flask import Flask, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Blogly
from users import Users

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iamlou'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()


@app.route("/")
def homepage():
    """Returns the home page"""
    return redirect("/users")


@app.route("/users")
def show_all_users():
    """ Shows all users """
    users = Blogly.query.all()
    return render_template("users.html", users=users)


@app.route("/users/new")
def add_new_user():
    """Shows the add new user form"""
    return render_template("new_user.html")


@app.route("/users/<int:id>")
def get_user_details(id):
    """Returns user detaisl"""
    user = Blogly.query.get(id)
    return render_template("user_details.html", user=user)


@app.route("/users/<int:id>/edit")
def edit_user_details(id):
    """Edit user details"""
    user = Blogly.query.get(id)
    return render_template("user_edit.html", user=user)


@app.route("/users/<int:id>/delete", methods=["POST"])
def delete_user(id):
    """Deletes user from the database"""
    user = Blogly.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/new", methods=["POST"])
def add_user_to_db():
    """Add the user to the database"""
    user = Users(request.form['first_name'],
                 request.form['last_name'],
                 request.form['image_url']
                 )
    user.add_user()
    return redirect("/users")


@app.route("/users/<int:id>/edit", methods=["POST"])
def update_user_to_db(id):
    """Update user details to the database"""
    # Get existing user data
    user = Users(request.form['first_name'],
                 request.form['last_name'],
                 request.form['image_url']
                 )
    user.update_user(id)
    return redirect(f"/users/{id}")
