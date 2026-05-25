import unittest
from app import app

class FlaskTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index_page(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

    def test_captcha_created(self):
        with self.client as client:
            client.get('/')

            with client.session_transaction() as session:
                self.assertIn("answer", session)
                self.assertIn("captcha_text", session)

    def test_correct_captcha(self):
        with self.client as client:
            client.get('/')

            with client.session_transaction() as session:
                answer = session["answer"]

            response = client.post(
                '/',
                data={"captcha": str(answer)}
            )

            self.assertEqual(response.status_code, 302)

    def test_wrong_captcha(self):
        with self.client as client:
            client.get('/')

            response = client.post(
                '/',
                data={"captcha": "999"}
            )

            self.assertEqual(response.status_code, 200)
            self.assertIn(
                "Неправильно".encode('utf-8'),
                response.data
            )


if __name__ == '__main__':
    unittest.main()