import json
from unittest import TestCase, mock
from fastapi.testclient import TestClient
from app.main import app


class TestEmployeeManagementSystem(TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @mock.patch('app.connector.Connector.read_all')
    def test_read_table_success(self, mock_read_all):
        mock_read_all.return_value = [{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Smith'}]
        response = self.client.get('/employee')
        assert response.status_code == 200
        assert response.json() == [{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Smith'}]

    @mock.patch('app.connector.Connector.write')
    def test_create_table_success(self, mock_write):
        rows = [{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Smith'}]
        response = self.client.post('/employee', json=rows)
        assert response.status_code == 200
        mock_write.assert_called_once_with(rows)

    def test_create_table_failure(self):
        rows = [{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Smith'}] * 1001
        response = self.client.post('/employee', json=rows)
        assert response.status_code == 400
        assert response.json() == {'detail': 'Invalid batch size'}

    def test_read_table_failure(self):
        response = self.client.get('/non_existent_table')
        assert response.status_code == 404
        assert response.json() == {'detail': 'Table not found'}

    def test_put_table_failure(self):
        rows = [{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Smith'}]
        response = self.client.put('/employee', json=rows)
        assert response.status_code == 405
        assert response.json() == {'detail': 'Not allowed response'}

    def test_delete_table_failure(self):
        rows = [{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Smith'}]
        response = self.client.delete('/employee', json=rows)
        assert response.status_code == 405
        assert response.json() == {'detail': 'Not allowed response'}