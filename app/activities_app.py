

from src.activity import Activity
from flask import Flask, flash, render_template, request, redirect, session, url_for, Blueprint

from src.database import Database
activities_blueprint = Blueprint('activities_blueprint', __name__)
db = Database().db

def get_trip_cost():
	return "select sum(price) from trip_common  where username=\"" + (session['username']) + "\"and is_booked = false;"

def get_all_activities_in_a_trip():
	# return "select activity_date, activity_name, cost, activity_start_time, activity_end_time, activity_id from activity natural join trip where username = '" + session['username'] + "' and is_booked = false;"
	return "select * from trip_common where username = '" + session['username'] + "' and is_booked = false;";


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
			return render_template("home.html", session=session, users=users, attractions=attractions, no_trip="Here, you can start making your first trip!")
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
#                        Activities                                 #
#####################################################################

def add_attraction_to_trip(attraction_name, activity_name, start_time, end_time, date, cost):
	return "insert into activity (activity_name, activity_start_time, activity_end_time, activity_date, attraction_name, username, trip_id, cost) values ('" + activity_name + "', '" + start_time + "', '" + end_time + "', '" + date + "', '" + attraction_name + "', '" + session['username'] + "', " + str(session['current_trip_id']) + ", " + str(cost) + ");"



def get_attractions_data():
	db = Database().db
	cursor = db.cursor()
	cursor.execute("select * from activities;")
	attractions = [dict(name=row[1], description=row[2], address=row[3],price=row[4]) for row in cursor.fetchall()]
	return attractions

# Shows all available attractions.
@activities_blueprint.route('/attractions')
def attractions():

	attractions = get_attractions_data()
	return render_template('attractions.html', items=attractions, session=session)

# Receive attraction data to turn into an activity
@activities_blueprint.route('/add-to-trip/<attraction_index>', methods=['POST'])
def add_to_trip(attraction_index):

	# TODO: Check if the attraction_name is on list of attractions
	print(session['current_trip_id'])
	if 'current_trip_id' not in session or not session['current_trip_id']:
		return create_trip(no_error=False)
	db = Database().db
	cursor = db.cursor()

	# Get attraction data
	cursor.execute("select * from activities;")
	attractions = [dict(name=row[1], description=row[2], address=row[3],price=row[4]) for row in cursor.fetchall()]
	attraction_name = attractions[int(attraction_index) - 1]['name']
	db.commit()
	name = attractions[int(attraction_index) - 1]['name']
	price = attractions[int(attraction_index) - 1]['price']
	values = (session['current_trip_id'],name,price, session['username'], 0)
	query_trip_common = "INSERT INTO trip_common ( trip_trip_id, name ,price, username, is_booked) VALUES (%s, %s, %s, %s, %s)"
	cursor.execute(query_trip_common, values)
	db.commit()
	query = get_all_activities_in_a_trip()
	cursor.execute(query)
	activities = [dict(id = row[0], name=row[2], number=row[3],price=row[4]) for row in cursor.fetchall()] # TODO: Correctly map activity info.
	# Calculate total cost of trip
	query = get_trip_cost()
	cursor.execute(query)
	amount = cursor.fetchall()[0][0]
	# amount = 0
	total_cost = str(amount)
	return render_template('trip.html', items=activities, session=session, total_cost=total_cost)

# Insert activity into database
@activities_blueprint.route('/create-activity', methods=['POST', 'GET'])
def create_activity():

	if 'current_trip_id' not in session or not session['current_trip_id']:
		return create_trip(no_error=False)

	# Get activity field data.
	attraction_name = request.form['attraction_name']
	activity_name = request.form['activity_name']
	start_time = request.form['start_time']
	end_time = request.form['end_time']
	date = request.form['date']
	cost = request.form['cost'][1:]

	# Add attraction to trip
	db = Database().db
	cursor = db.cursor()
	query = add_attraction_to_trip(attraction_name, activity_name, start_time, end_time, date, cost)
	
	cursor.execute(query)
	db.commit()

	success = attraction_name + " added to My Trip!"
	attractions = get_attractions_data()
	return render_template('attractions.html', items=attractions, session=session, success=success)

# Delete an attraction
@activities_blueprint.route('/delete-attraction/<attraction_index>')
def delete_attraction(attraction_index):

	# Get attraction_name
	db = Database().db
	cursor = db.cursor()
	cursor.execute("select attraction.attraction_name from attraction natural join address;")
	attraction_name = cursor.fetchall()[int(attraction_index) - 1][0]

	# Delete from database
	cursor.execute("delete from attraction where attraction_name='" + attraction_name + "';")
	db.commit()
	return redirect(url_for('home'))


@activities_blueprint.route('/add-activity', methods=['GET'])
def add_activityt():
	return render_template('add_activity.html')

@activities_blueprint.route('/activity-create', methods=['POST'])
def create_activity():
    
	if request.method == 'POST':
		activity_name = request.form['activity_name']
		activity_desc = request.form['activity_desc']
		activity_address = request.form['activity_address']
		price = request.form['price']
		price = request.form['price']
		activity_object = Activity(activity_name, activity_desc, activity_address,price)
		activity_object.save()
		return redirect('/attractions')
	return render_template('add_activity.html')