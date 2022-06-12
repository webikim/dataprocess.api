import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from dpapi.db import models
from dpapi.main import app
from dpapi.routers.login import create_access_token


class DpAPITestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.script_data = {
            'name': 'test job',
            'script_type': '1',
            'content': 'test content',
            'note': 'test note'
        }
        self.script = models.Script(name=self.script_data['name'],
                                    script_type=self.script_data['script_type'],
                                    content=self.script_data['content'],
                                    note=self.script_data['note'])
        self.run_data = {
            'script_id': '1',
            'requested': '2022'
        }
        self.token = create_access_token(data={"sub": '1'})

    def test_script_create(self):
        with patch('dpapi.db.dp_crud.create_script') as mock_create_script:
            mock_create_script.return_value = self.script_data
            response = self.client.post('/dpapi/script',
                                        json=self.script_data,
                                        headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(200, response.status_code)
        with patch('dpapi.db.dp_crud.update_script') as mock_updatescript:
            mock_updatescript.return_value = self.script_data
            response = self.client.post('/dpapi/script',
                                        json=dict(self.script_data, **{'id': 1}),
                                        headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(200, response.status_code)

    def test_script_get(self):
        with patch('dpapi.db.dp_crud.get_script') as mock_get_script:
            mock_get_script.return_value = self.script
            response = self.client.get('/dpapi/script',
                                       params={'script_id': 1},
                                       headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(200, response.status_code)

    def test_script_delete(self):
        with patch('dpapi.db.dp_crud.delete_script') as mock_delete_script:
            mock_delete_script.return_value = 'OK'
            response = self.client.delete('/dpapi/script',
                                          params={'script_id': 1},
                                          headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(200, response.status_code)

    def test_run_create(self):
        with patch('dpapi.db.dp_crud.create_runlog') as mock_create_runlog:
            mock_create_runlog.return_value = self.run_data
            response = self.client.post('/dpapi/run',
                                        json=self.run_data,
                                        headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
