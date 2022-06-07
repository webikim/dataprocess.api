import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from dpapi.db import models
from dpapi.main import app
from dpapi.routers.login import create_access_token


class DpAPITestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.data = {
            'name': 'test job',
            'content': 'test content',
            'note': 'test note'
        }
        self.script = models.Script(name=self.data['name'],
                                    content=self.data['content'],
                                    note=self.data['note'])
        self.token = create_access_token(data={"sub": '1'})

    def test_script_create(self):
        with patch('dpapi.db.dp_crud.create_script') as mock_createscript:
            mock_createscript.return_value = self.data
            response = self.client.post('/dpapi/script',
                                        json=self.data,
                                        headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(200, response.status_code)
        with patch('dpapi.db.dp_crud.update_script') as mock_updatescript:
            mock_updatescript.return_value = self.data
            response = self.client.post('/dpapi/script',
                                        json=dict(self.data, **{'script_id': 1}),
                                        headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(200, response.status_code)

    def test_script_get(self):
        with patch('dpapi.db.dp_crud.get_script') as mock_getscript:
            mock_getscript.return_value = self.script
            response = self.client.get('/dpapi/script',
                                       headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(200, response.status_code)

    def test_script_delete(self):
        with patch('dpapi.db.dp_crud.delete_script') as mock_deletescript:
            mock_deletescript.return_value = 'OK'
            response = self.client.delete('/dpapi/script',
                                          params={'script_id': 1},
                                          headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
