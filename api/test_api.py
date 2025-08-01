import unittest
import app

class TestTaskAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_create_task(self):
        rv = self.app.post('/tasks', json={"title": "test", "description": "test desc", "assignee": "user1"})
        self.assertEqual(rv.status_code, 201)

    def test_get_tasks(self):
        rv = self.app.get('/tasks/user1')
        self.assertEqual(rv.status_code, 200)

if __name__ == '__main__':
    unittest.main()
