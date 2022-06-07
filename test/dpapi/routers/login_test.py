import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from dpapi.db import models
from dpapi.main import app
from dpapi.routers.login import get_password_hash


class LoginTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.data = {
            'full_name': 'test this',
            'email': 'test2@@email.com',
            'password': 'password'
        }
        self.user = models.User(email=self.data['email'],
                                full_name=self.data['full_name'],
                                hashed_password=get_password_hash(self.data['password']))

    def test_create_user(self):
        with patch('dpapi.db.user_crud.get_user_by_email') as mock_getuser:
            with patch('dpapi.db.user_crud.save_user') as mock_saveuser:
                mock_getuser.return_value = self.user
                mock_saveuser.return_value = self.user
                response = self.client.post('/users/create', json=self.data)
                self.assertEqual(409, response.status_code)
                mock_getuser.reset_mock()
                mock_getuser.return_value = None
                response = self.client.post('/users/create', json=self.data)
                self.assertEqual(200, response.status_code)

    def test_login(self):
        with patch('dpapi.db.user_crud.get_user_by_email') as mock_get_user:
            mock_get_user.return_value = self.user
            response = self.client.post('/login', json={'email': 'test@email.com', 'password': 'password'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.text.find('access_token') > 0, True)


if __name__ == '__main__':
    unittest.main()
