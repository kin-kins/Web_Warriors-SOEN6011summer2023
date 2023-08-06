from src.database import Database


class Activity:
    def __init__(self, name, description, address, price,skill):
        self.name = name
        self.description = description
        self.address = address
        self.price = price
        self.skill = skill
        
    def save(self):
        query = "INSERT IGNORE INTO job_posting (company_name ,description,address, salary,skills) VALUES (%s, %s, %s, %s,%s)"
        values = (self.name,self.description,self.address,self.price,self.skill)
        print(query, values)
        db = Database().get_db()
        cursor = db.cursor()
        cursor.execute(query, values)
        db.commit()
