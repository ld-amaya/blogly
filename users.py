from models import User, db


class Users():

    def __init__(self, first_name, last_name, image_url=""):
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url

    def add_user(self):
        """Add new user to the database"""
        user = User(first_name=self.first_name,
                    last_name=self.last_name,
                    image_url=self.image_url)

        db.session.add(user)
        db.session.commit()

    def update_user(self, id):
        """Update User"""
        user = User.query.get(id)
        user.first_name = self.first_name
        user.last_name = self.last_name
        user.image_url = self.image_url
        db.session.add(user)
        db.session.commit()
