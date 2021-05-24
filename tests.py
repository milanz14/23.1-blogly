from unittest import TestCase
from app import app
from models import db, User, Post

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

# class PostModelTestCase(TestCase):
#     """ Tests for Post model and any routes that have to do with user posts """
#     def setUp(self):
#         """ clean up any existing posts """
#         Post.query.delete()
#         User.query.delete()
#         test_user= User(first_name='Test', last_name='User')
#         db.session.add(test_user)
#         db.session.commit()
#         test_post = Post(title='Test', content='Test Post Content',user_id=test_user.id)
#         db.session.add(test_post)
#         db.session.commit()
#         self.post = test_post
#         self.post_id = test_post.id
        
#     def tearDown(self):
#         """ clean up fouled transactions """
#         db.session.rollback()

#     def test_show_users_posts(self):
#         """ test the posts seen on a user's page -
#         need to create a test user in the setUp method """
#         with app.test_client() as client:
#             pass

#     def test_posts_details(self):
#         """ test post details page """
#         with app.test_client() as client:
#             resp = client.get(f'/posts/{self.post_id}')
#             html = resp.get_data(as_text=True)
#             self.assertEqual(resp.status_code, 200)
#             self.assertIn('<h3>Test</h3>', html)
    
#     def test_edit_post(self):
#         """ test the edit post page """
#         with app.test_client() as client:
#             d = {"title": "Test","content":"this is the content"}
#             resp = client.post(f'/users/{self.post_id}/edit', data=d, follow_redirects=True)
#             html = resp.get_data(as_text=True)
#             self.assertEqual(resp.status_code, 200)
#             self.assertIn('<h3>Test</h3>', html)