from src.database import Database


class Activity:
    def __init__(self, name, description, address, price):
        self.name = name
        self.description = description
        self.address = address
        self.price = price
        
    def save(self):
        query = "INSERT INTO activities ( activity_name,description,address,price) VALUES (%s,%s,%s,%s)"
        values = (self.name,self.description,self.address,self.price)
        print(query, values)
        db = Database().get_db()
        cursor = db.cursor()
        cursor.execute(query, values)
        db.commit()
