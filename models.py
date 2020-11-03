from flask_sqlalchemy import SQLAlchemy

# Initialize variable to run SQLAlchemy
db = SQLAlchemy()


def connect_db(app):
    """Connecting to the database"""

    db.app = app
    db.init_app(app)


class Blogly(db.Model):
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
