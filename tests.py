from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bloglydb_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """ Tests for model for Users """
    def setUp(self):
        """ clean up any existing users """
        User.query.delete()
        test_user = User(first_name='Test',last_name='User')
        db.session.add(test_user)
        db.session.commit()
        self.user = test_user
        self.user_id = test_user.id
    
    def tearDown(self):
        """ clean up any fouled transaction """
        db.session.rollback()

    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users Page</h1>', html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h2>User Details</h2>', html)
    
    def test_add_new_user(self):
        with app.test_client() as client:
            d = {"firstname": "Test", "lastname": "User"}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users Page</h1>', html)
    
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get(f'users/{self.user_id}/delete')
            html = resp.get_data(as_text=True)
            self.assertNotIn('Test User', html)