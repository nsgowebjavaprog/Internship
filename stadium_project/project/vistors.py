import database
class Vistor:
    def __init__(self, name, age, email, password, phno, orders=[]) -> None:
        self.data = {
            "name" : name,
            "age" : age,
            "email" : email,
            "password" : password,
            "phno" : phno,
            "orders": orders,
        }
        self.__create_user()

    def __create_user(self):
        db = database.JsonDB("data.json")
        data = db.read("visitors")
        if data == None:
            db.create({"visitors" : {}})
        data = db.read("visitors")
        data["visitors"].update({self.data["name"] : self.data})
        db.update("visitors", data)

    def update_user(self):
        key = input("update : ")
        value = input("new value : ")
        if (key == "name"):
            print("can't change name as it is id of user")
        db = database.JsonDB("data.json")
        data = db.read("visitors")
        data["visitors"][self.data["name"]][key] = value
        self.data[key] = value
        db.update("visitors", data)
        db.save_data()

    def delete_user(self):
        db = database.JsonDB("data.json")
        data = db.read("visitors")
        data["visitors"].pop(self.data["name"])
        db.update("visitors", data)
        db.save_data()
    
    def user_details(self):
        return self.data
    
    def save_user(self):
        db = database.JsonDB("data.json")
        data = db.read("visitors")
        data["visitors"][self.data["name"]] = self.data 
        db.update("visitors", data)
        db.save_data()

    def update_orders(self, orders):
        db = database.JsonDB("data.json")
        data = db.read("visitors")
        data["visitors"][self.data["name"]]["orders"] += [orders]
        self.data["orders"] = data["visitors"][self.data["name"]]["orders"]
        db.update("visitors", data)
        db.save_data()
    
    @staticmethod
    def get_user(name):
        db = database.JsonDB("data.json")
        data = db.read("visitors")
        if name not in data["visitors"].keys():
            print(f"no visitor named {name}")
            return None
        user_data = data["visitors"][name]
        return Vistor(user_data["name"], user_data["age"], user_data["email"], user_data["password"], user_data["phno"], user_data["orders"])
        
#visitors
import unittest

class TestVistor(unittest.TestCase):
    def setUp(self):
       
        self.db_file = "data.json"
        database.JsonDB(self.db_file)

    def tearDown(self):
        
        import os
        os.remove(self.db_file)

    def test_init(self):
       
        v = Vistor("John Doe", "30", "johndoe@example.com", "password", "1234567890")
        visitor_details = v.user_details()
        self.assertEqual(visitor_details["name"], "John Doe")
        self.assertEqual(visitor_details["age"], "30")
        self.assertEqual(visitor_details["email"], "johndoe@example.com")
        self.assertEqual(visitor_details["password"], "password")
        self.assertEqual(visitor_details["phno"], "1234567890")

    def test_create_user(self):
       
        visitor = Vistor("Jane Doe", "25", "janedoe@example.com", "password", "0987654321")
        self.assertIn("Jane Doe", database.JsonDB(self.db_file).read("visitors")["visitors"].keys())

    def test_update_user(self):
        
        visitor = Vistor("Jane Doe", "25", "janedoe@example.com", "password", "0987654321")
        visitor.update_user()
        self.assertEqual(visitor.data["age"], "30")

    def test_delete_user(self):
        
        visitor = Vistor("Jane Doe", 25, "janedoe@example.com", "password", "0987654321")
        visitor.delete_user()
        self.assertNotIn("Jane Doe", database.JsonDB(self.db_file).read("visitors")["visitors"].keys())

    def test_user_details(self):
       
        visitor = Vistor("Jane Doe", 25, "janedoe@example.com", "password", "0987654321")
        self.assertEqual(visitor.user_details(), visitor.data)

    def test_save_user(self):
       
        visitor = Vistor("Jane Doe", 25, "janedoe@example.com", "password", "0987654321")
        visitor.save_user()
        self.assertIn("Jane Doe", database.JsonDB(self.db_file).read("visitors")["visitors"])

    def test_update_orders(self):
        
        visitor = Vistor("Jane Doe", 25, "janedoe@example.com", "password", "0987654321")
        visitor.update_orders("order1")
        self.assertEqual(visitor.user_details()["orders"], ["order1"])

    def test_get_user(self):
      
        visitor = Vistor("Jane Doe", 25, "janedoe@example.com", "password", "0987654321")
        self.assertEqual(Vistor.get_user("Jane Doe").data, visitor.data)

if __name__ == "__main__":
    unittest.main()
        