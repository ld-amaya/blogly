import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize variable to run SQLAlchemy
db = SQLAlchemy()


def connect_db(app):
    """Connecting to the database"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Creates the blogly table"""

    __tablename__ = "users"

    def __repr__(self):
        return (f"id: {self.id}, first name ={self.first_name}, last_name ={self.last_name}, image_url={self.image_url}")

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(25),
                           nullable=False)

    last_name = db.Column(db.String(25),
                          nullable=False)

    image_url = db.Column(db.Text(),
                          nullable=False)

    post = db.relationship("Post",
                           backref="user",
                           cascade="all,delete-orphan")

    @property
    def fullname(self):
        """Returns the full name of the user"""
        return (f"{self.first_name} {self.last_name}")


class Post(db.Model):
    """Creates the model table"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(50),
                      nullable=False)

    content = db.Column(db.Text,
                        nullable=False)

    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    @property
    def this_date(self):
        """Generates a formatted date"""

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")


class Tag(db.Model):
    """Creates a tag model"""

    __tablename__ = "tags"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(50),
                     nullable=False,
                     unique=True)

    post = db.relationship("Post",
                           secondary="post_tags",
                           backref="tag")


class PostTag(db.Model):
    """Creates a post_tag model and relationship"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)

    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)
