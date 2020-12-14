from unittest import TestCase
from app import app
from models import db, User, Post
from users import Users
from flask import jsonify
import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class BloglyModelTestCase(TestCase):
    """Test for User Model"""

    def setUp(self):

        # Add data to database
        user1 = User(first_name="user", last_name="one",
                     image_url="https://images.unsplash.com/photo-1499358517822-d8578907a095?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=700&q=60")
        user2 = User(first_name="user", last_name="two",
                     image_url="https://images.unsplash.com/photo-1499358517822-d8578907a095?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=700&q=60")

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # add post to database
        post1 = Post(title="First Post",
                     content="First post content",
                     user_id="1")
        post2 = Post(title="Second Post",
                     content="Second post content",
                     user_id="2")

        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()

        self.user_id = user1.id
        self.user = user1

    def tearDown(self):
        db.session.rollback()

    def test_index(self):
        """Test home get request"""
        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h1>Recent Posts</h1>", html)
            self.assertIn("First Post", html)
            self.assertIn('Created by <a href="/users/1"> user one </a>', html)
            self.assertIn("Second post content", html)

    def test_new_user_form(self):
        """Test new_user.html"""
        with app.test_client() as client:
            response = client.get("/users/new")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<label for="first_name">First Name</label>', html)

    def test_user_details(self):
        """Test user_details.html and posts"""
        with app.test_client() as client:
            response = client.get(f"/users/1")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h3> user one</h3>", html)
            self.assertIn("First Post", html)

    def test_add_user(self):
        """Test user adding"""

        with app.test_client() as client:
            user3 = {"first_name": "thirdy",
                     "last_name": "three", "image_url": "http://"}
            response = client.post(
                f"/users/new", data=user3, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("thirdy three", html)

    def test_delete_user(self):
        """Test user deleting"""

        with app.test_client() as client:
            response = client.post(
                f"/users/{self.user_id}/delete", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone("user one", html)

    ##### TEST POST REQUESTS ########################
    def test_add_post(self):
        """Test add post"""

        post = {"title": "Added Post",
                "content": "Added post content",
                "user_id": "1"}
        with app.test_client() as client:
            response = client.post(
                "/users/1/posts/new", data=post, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Added Post", html)

    def test_delete_post(self):
        """test delete post"""
        with app.test_client() as client:
            response = client.post(f"/posts/3/delete", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Successfully deleted the post Added Post", html)
