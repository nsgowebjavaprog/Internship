import json
import os

class JsonDB:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        else:
            return []

    def create(self, dictionary):
        self.data.append(dictionary)
        self.save_data()

    def read(self, key=None) -> dict | None:
        if key is None:
            return self.data
        else:
            for dictionary in self.data:
                if key in dictionary:
                    return dictionary
            return None

    def update(self, key, dictionary):
        for i, d in enumerate(self.data):
            if key in d:
                self.data[i] = dictionary
                self.save_data()
                return
        raise KeyError(f"Key '{key}' not found")

    def delete(self, key):
        for i, d in enumerate(self.data):
            if key in d:
                del self.data[i]
                self.save_data()
                return
        raise KeyError(f"Key '{key}' not found")

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)
            
# unittest
#data base
import unittest
import json
import os

class TestJsonDB(unittest.TestCase):
    def setUp(self):
        self.filename = 'test.json'
        self.db = JsonDB(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_load_data(self):
        # Test that load_data returns an empty list if the file doesn't exist
        self.assertEqual(self.db.data, [])

        # Test that load_data returns the correct data if the file exists
        with open(self.filename, 'w') as f:
            json.dump([{'key': 'value'}], f)
        self.db = JsonDB(self.filename)
        self.assertEqual(self.db.data, [{'key': 'value'}])

    def test_create(self):
        # Test that create adds a new dictionary to the data list
        self.db.create({'key': 'value'})
        self.assertEqual(self.db.data, [{'key': 'value'}])

        # Test that create saves the data to the file
        with open(self.filename, 'r') as f:
            self.assertEqual(json.load(f), [{'key': 'value'}])

    def test_read(self):
        # Test that read returns the entire data list if no key is provided
        self.db.data = [{'key': 'value1'}, {'key': 'value2'}]
        self.assertEqual(self.db.read(), [{'key': 'value1'}, {'key': 'value2'}])

        # Test that read returns the correct dictionary if a key is provided
        self.assertEqual(self.db.read('key'), {'key': 'value1'})

        # Test that read returns None if the key is not found
        self.assertIsNone(self.db.read('nonexistent_key'))

    def test_update(self):
        # Test that update updates the correct dictionary
        self.db.data = [{'key': 'value1'}, {'key': 'value2'}]
        self.db.update('key', {'key': 'new_value'})
        self.assertEqual(self.db.data, [{'key': 'new_value'}, {'key': 'value2'}])

        # Test that update raises a KeyError if the key is not found
        with self.assertRaises(KeyError):
            self.db.update('nonexistent_key', {'key': 'new_value'})

    def test_delete(self):
        # Test that delete removes the correct dictionary
        self.db.data = [{'key': 'value1'}, {'key': 'value2'}]
        self.db.delete('key')
        self.assertEqual(self.db.data, [{'key': 'value2'}])

        # Test that delete raises a KeyError if the key is not found
        with self.assertRaises(KeyError):
            self.db.delete('nonexistent_key')

    def test_save_data(self):
        # Test that save_data saves the data to the file
        self.db.data = [{'key': 'value'}]
        self.db.save_data()
        with open(self.filename, 'r') as f:
            self.assertEqual(json.load(f), [{'key': 'value'}])

if __name__ == '__main__':
    unittest.main()


