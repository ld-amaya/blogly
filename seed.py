from models import User, db, Post, Tag, PostTag
from app import app


# Create and drop all the tables
db.drop_all()
db.create_all()

User.query.delete()

# Create dummy users
user1 = User(first_name='Juan', last_name='Banayad',
             image_url='https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80')
user2 = User(first_name='Dolphy', last_name='Quizon',
             image_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80')
user3 = User(first_name='John', last_name='Porontong',
             image_url='https://images.unsplash.com/photo-1531123897727-8f129e1688ce?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80')

# Add Users
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Create dummy blog posts
blog1 = Post(title='First Blog',
             content='This is my first blog',
             user_id=1)

blog2 = Post(title='Amazing Blog',
             content='This is my Amazing blog',
             user_id=1)


blog3 = Post(title='Perfect Blog',
             content='This is my Perfect blog',
             user_id=2)


blog4 = Post(title='Happy Blog',
             content='This is my Happy blog',
             user_id=3)

# Add Blog
db.session.add(blog1)
db.session.add(blog2)
db.session.add(blog3)
db.session.add(blog4)

# Commit database
db.session.commit()


# Create dummy tags
tag1 = Tag(name='Biking')
tag2 = Tag(name='Hiking')

db.session.add(tag1)
db.session.add(tag2)
db.session.commit()


# create post_tag
posttag1 = PostTag(post_id=1,
                   tag_id=1)
posttag2 = PostTag(post_id=2,
                   tag_id=2)

db.session.add(posttag1)
db.session.add(posttag2)
db.session.commit()
