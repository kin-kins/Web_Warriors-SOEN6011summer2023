from src.database import Database

class Flight:
    def __init__(self, airline_name,flight_number, departure_airport,departure_date, departure_time, arrival_airport, duration, price):
        self.flight_number = flight_number
        self.airline_name = airline_name
        self.departure_airport = departure_airport
        self.departure_time = departure_time
        self.departure_date = departure_date
        self.arrival_airport = arrival_airport
        self.duration = duration
        self.price = price
        self.db = Database().get_db()
        self.cursor = self.db.cursor()

    def check_sql_string(self, sql, values):
        unique = "%PARAMETER%"
        sql = sql.replace("?", unique)
        for v in values: sql = sql.replace(unique, repr(v), 1)
        return sql

    def get_all_flights(self):
        query = "SELECT * FROM flights"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        flights = []
        for flight in result:
            flights.append(Flight(flight[0], flight[1], flight[2], flight[3], flight[4], flight[5]))
        return flights

    def get_flight_by_flight_number(self, flight_number):
        query = "SELECT * FROM flights WHERE flight_number = %s"
        self.cursor.execute(query, (flight_number,))
        result = self.cursor.fetchone()
        if result:
            return Flight(result[0], result[1], result[2], result[3], result[4], result[5])
        return None

    def save(self):
        query = "INSERT INTO flights ( airline_name,flight_number, departure_airport,departure_date, departure_time, arrival_airport, duration, price) VALUES (%s, %s, %s, %s, %s, %s,%s, %s)"
        values = (self.airline_name, self.flight_number, self.departure_airport,self.departure_date, self.departure_time,
                  self.arrival_airport, self.duration, self.price)
        print(query, values)
        print("-------------------")
        print(self.check_sql_string(query, values))
        self.cursor.execute(query, values)
        self.db.commit()

    def update(self):
        query = "UPDATE flights SET airline = %s, departure_airport = %s, " \
                "departure_datetime = %s, arrival_airport = %s, duration = %s WHERE flight_number = %s"
        values = (self.airline, self.departure_airport, self.departure_datetime,
                  self.arrival_airport, self.duration, self.flight_number)
        self.cursor.execute(query, values)
        self.db.commit()

    def delete(self):
        query = "DELETE FROM flights WHERE flight_number = %s"
        self.cursor.execute(query, (self.flight_number,))
        self.db.commit()
