from app import app, Contact, NewEmail
import unittest


class FlaskTestCase(unittest.TestCase):
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        contact = Contact('test_user', 'test@gmail.com', None, None)
        self.assertEqual(contact.username, 'test_user')

    def test_add_email(self):
        contact = Contact('test_user', 'test@gmail.com', None, None)
        add_email = NewEmail('test2@gmail.com', contact.id)
        self.assertEqual(contact.username, 'test_user')
        self.assertEqual(add_email.new_email, 'test2@gmail.com')
        self.assertEqual(add_email.contact_id, contact.id)


if __name__ == 'main':
    unittest.main()
