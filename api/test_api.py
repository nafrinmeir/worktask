import unittest
import app
from pymongo import MongoClient

class TestTaskAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests. Ensure user1 has at least one task."""
        cls.client = app.app.test_client()

        # Ensure MongoDB is available and clean the collection
        mongo_client = MongoClient("mongodb://localhost:27017/")
        db = mongo_client["TaskListTest"]
        cls.task_collection = db["AllTaskTest"]

        # Clean up old test tasks
        cls.task_collection.delete_many({"assignee": "user1", "title": "test"})

        # Insert at least one task for user1
        cls.task_collection.insert_one({
            "title": "test",
            "description": "setup task",
            "assignee": "user1"
        })

    def test_create_task(self):
        rv = self.client.post('/tasks', json={
            "title": "test",
            "description": "test desc",
            "assignee": "user1"
        })
        self.assertEqual(rv.status_code, 201)

    def test_get_tasks(self):
        rv = self.client.get('/tasks/user1')
        self.assertEqual(rv.status_code, 200)
        self.assertIsInstance(rv.json, list)
        self.assertGreaterEqual(len(rv.json), 1)

if __name__ == '__main__':
    unittest.main()
