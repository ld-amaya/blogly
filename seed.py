from models import Blogly, db
from app import app


# Create and drop all the tables
db.drop_all()
db.create_all()

Blogly.query.delete()

# Create dummy users
user1 = Users(first_name='Juan', last_name='Banayad',
              image_url='https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80')
user2 = Users(first_name='Dolphy', last_name='Quizon',
              image_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80')
user3 = Users(first_name='John', last_name='Porontong',
              image_url='https://images.unsplash.com/photo-1531123897727-8f129e1688ce?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80')

# Add Users
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Commit database
db.session.commit()
