from src.flight import Flight
from flask import Flask, flash, render_template, request, redirect, session, url_for
from flask_wtf import Form
import hashlib
import locale
import pymysql
import time
from src.customer import Customer
from src.database import Database
from datetime import datetime
import app.resume as resume_app
import app.activities_app  as activities_app
import app.login_app as login_app
import app.booking_history as booking_history_app

app = Flask(__name__)
app.config['SECRET_KEY'] = '8ffe05624dfe0efdf7c7f67288d4f4ce5005e0dfb6a1bc48366ef9906dd0586e'
app.register_blueprint(resume_app.resume_blueprint, url_prefix='/')
app.register_blueprint(activities_app.activities_blueprint, url_prefix='/')
app.register_blueprint(login_app.login_blueprint, url_prefix='/')
app.register_blueprint(booking_history_app.booking_blueprint, url_prefix='/')
dbOb= Database()



#####################################################################
#                          SQL Queries                              #
#####################################################################

def get_attractions_data():

	cursor = db.cursor()
	cursor.execute("select * from activities;")
	attractions = [dict(name=row[1], description=row[2], address=row[3],price=row[4]) for row in cursor.fetchall()]
	return attractions

def view_completed_attractions_query():
	 return "select activity_date, attraction.attraction_name, description from activity natural join attraction where activity.username = '" + session['username'] + "' and ((activity_date = CURDATE() and activity_end_time <= CURTIME()) or activity_date < CURDATE());"

def get_trip_cost():
	return "select sum(cost) from activity join trip using (trip_id) where trip_id = " + str(session['current_trip_id']) + ";"

def get_all_activities_in_a_trip():
	return "select activity_date, activity_name, cost, activity_start_time, activity_end_time, activity_id from activity natural join trip where username = '" + session['username'] + "' and is_booked = false;";

def get_current_trip_id():
	return "select trip_id from trip natural join user where trip.is_booked=false and user.username='" + session['username'] + "';"

def add_attraction_to_trip(attraction_name, activity_name, start_time, end_time, date, cost):
	return "insert into activity (activity_name, activity_start_time, activity_end_time, activity_date, attraction_name, username, trip_id, cost) values ('" + activity_name + "', '" + start_time + "', '" + end_time + "', '" + date + "', '" + attraction_name + "', '" + session['username'] + "', " + str(session['current_trip_id']) + ", " + str(cost) + ");"


def create_trip(no_error):

	# Query database when user is admin for admin panel
	if session['is_admin']:

		# Get user table information.
		db = Database().db
		cursor = db.cursor()
		cursor.execute("select * from user;")
		users = [dict(is_admin="Yes" if row[3] == 1 else "No", username=row[0], password=row[1], first_name=row[4], last_name=row[5], email=row[2], suspended="Yes" if row[7] == 1 else "No") for row in cursor.fetchall()]

		# Get attraction table information.
		attractions = get_attractions_data()

		if no_error:
			return render_template("home.html", session=session, users=users, attractions=attractions, no_trip="")
		else:
			return render_template("home.html", session=session, users=users, attractions=attractions, no_trip_error="You must first create a new trip!")

	# Not an admin
	if no_error:
		if 'current_trip_id' not in session or not session['current_trip_id']:
			return render_template("home.html", session=session, no_trip="Here, you can start making a new trip!")
		return render_template("home.html", session=session)
	else:
		return render_template("home.html", session=session, no_trip_error="You must first create a new trip!")



#####################################################################
#                         INDEX/HOME                                #
#####################################################################

# Visit site for first time. Pictures.
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

# Home page. Displays admin interface if user is admin.
@app.route('/home')
def home():

	# Disallow unlogged in users from requesting homepage.
	if 'username' not in session or session['username'] == '':
		return redirect(url_for('index'))
	return create_trip(no_error=True)

#####################################################################
#                          ADMIN PANEL                              #
#####################################################################

# Delete user from admin panel
@app.route('/delete-user/<username>')
def delete_user(username):
	
	db = Database().db
	cursor = db.cursor()
	cursor.execute("delete from user where username='" + username + "';")
	db.commit()

	return redirect(url_for('home'))

# Suspend user from admin panel
@app.route('/suspend-user/<username>')
def suspend_user(username):

	db = Database().db
	cursor = db.cursor()
	cursor.execute("select suspended from user where username='" + username + "';")
	if cursor.fetchall()[0][0] == 1:
		cursor.execute("update user set suspended=0 where username='" + username + "';")
	else:
		cursor.execute("update user set suspended=1 where username='" + username + "';")
	db.commit()

	return redirect(url_for('home'))

# Make user an Admin from admin panel
@app.route('/make-admin/<username>')
def make_admin(username):

	db = Database().db
	cursor = db.cursor()
	cursor.execute("update user set is_admin=1 where username='" + username + "';")
	db.commit()

	return redirect(url_for('home'))


#####################################################################
#                         MAIN APPLICATION                          #
#####################################################################

# Run the application
if __name__ == '__main__':
	db = Database().get_db()
	# Note: If your database uses a different password, enter it here.
	app.run(debug=True, host='0.0.0.0', port=8000)
	