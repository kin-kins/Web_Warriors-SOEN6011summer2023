import pymysql

class Database:
    
    def __init__(self):
        db_pass = 'dummy%123'

	# Make sure your database is started before running run.py
        db_name = 'team1'
        self.db = pymysql.connect(host='traveldatabase.cotbd4fsbm2q.us-east-1.rds.amazonaws.com', user='admin', passwd=db_pass, db=db_name)



    def get_db (self):
        return self.db
    
    def insert(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        
    def execute_with_values(self, query, values):
        cursor = self.db.cursor()
        cursor.execute(query, values)
        self.db.commit()
        cursor.close()
    
