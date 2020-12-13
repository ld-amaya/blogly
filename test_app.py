from unittest import TestCase
from app import app
from models import db, Blogly
from users import Users
from flask import jsonify

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class BloglyModelTestCase(TestCase):
    """Test for Blogly Model"""

    def setUp(self):
        """Clean up any existing users"""
        Blogly.query.delete()

        # Add data to database
        user1 = Blogly(first_name="user", last_name="one",
                       image_url="https://images.unsplash.com/photo-1499358517822-d8578907a095?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=700&q=60")
        user2 = Blogly(first_name="user", last_name="two",
                       image_url="https://images.unsplash.com/photo-1499358517822-d8578907a095?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=700&q=60")

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.user_id = user1.id
        self.user = user1

    def tearDown(self):
        db.session.rollback()

    def test_index(self):
        """Test home get request if forwarded to users.html"""
        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 302)

    def test_index_redirect(self):
        """Test home get request if forwarded to users.html"""
        with app.test_client() as client:
            response = client.get("/", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h1>List of users</h1>", html)
            self.assertIn("user one", html)
            self.assertIn("user two", html)

    def test_new_user_form(self):
        """Test new_user.html"""
        with app.test_client() as client:
            response = client.get("/users/new")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<label for="first_name">First Name</label>', html)

    def test_user_details(self):
        """Test user_details.html"""
        with app.test_client() as client:
            response = client.get(f"/users/{self.user_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h3> user <br/> one</h3>", html)

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

    def test_user_update(self):
        # add the user
        # udpate the user
        # test edit

    def test_delete_user(self):
        """Test user deleting"""

        with app.test_client() as client:
            response = client.post(
                f"/users/{self.user_id}/delete", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone("user one", html)
