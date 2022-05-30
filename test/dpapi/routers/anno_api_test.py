import unittest
from unittest.mock import patch, mock_open

from starlette.testclient import TestClient

from dpapi.main import app


class SiteRoutesCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def tearDown(self) -> None:
        pass

    def test_anno_get(self):
        with patch('builtins.open', mock_open(read_data='{"this": "from", "out_path": ["value"]}')) as mock_file:
            ret = self.client.get('/annoapi/anno/get?path=out&name=1070262.jpg')
        self.assertEqual('{"this":"from","out_path":["value"]}', ret.text)

    def test_anno_delete(self):
        with patch('os.remove') as mock_remove:
            ret = self.client.delete('/annoapi/anno/delete',
                                     json={'path': 'out', 'name': '1070262.json'},
                                     headers={"Authorization": 'token'})
        self.assertEqual('"OK"', ret.text)

    def test_anno_save(self):
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('os.mkdir'):
                ret = self.client.post('/annoapi/anno/save',
                                       json={'path': 'out', 'name': '1070262.json', 'data': {"json": "data"}})
        self.assertEqual('"OK"', ret.text)

    def test_list_dir(self):
        with patch('os.listdir') as mock_listdir:
            with patch('os.path.isdir') as mock_isdir:
                mock_listdir.return_value = ['dir1', 'dir2']
                mock_isdir.return_value = True
                ret = self.client.get('/annoapi/dir/list')
        self.assertEqual('["dir1","dir2"]', ret.text)

    def test_file_list(self):
        with patch('os.listdir') as mock_listdir:
            with patch('os.path.isdir') as mock_isdir:
                mock_listdir.return_value = ['file1.jpg', 'file2']
                mock_isdir.return_value = False
                ret = self.client.get('/annoapi/file/list?path=out')
        self.assertEqual('["file1.jpg"]', ret.text)

    def test_label_get(self):
        with patch('builtins.open', mock_open(read_data='{"this": "from", "label_path": ["value"]}')) as mock_file:
            ret = self.client.get('/annoapi/label/get?path=out&name=1070263.jpg')
        self.assertEqual('{"this":"from","label_path":["value"]}', ret.text)


if __name__ == '__main__':
    unittest.main()
