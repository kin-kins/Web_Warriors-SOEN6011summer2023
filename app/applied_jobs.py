from flask import Flask, flash, render_template, request, redirect, session, url_for, Blueprint
from src.database import Database
from app.jobs_posting import get_jp_data

booking_blueprint = Blueprint('booking_blueprint', __name__)

#####################################################################
#                          SQL Queries                              #
#####################################################################
def get_jobs_applied():
	# return "select activity_date, activity_name, cost, activity_start_time, activity_end_time, activity_id from activity natural join trip where username = '" + session['username'] + "' and is_booked = false;"
	if session['username']=="admin":
		return "select * from job_applied;"
	return "select * from job_applied where username = '" + session['username'] + "';"
 

db = Database().db

#####################################################################
#                               JOBS                                #
#####################################################################

# Shows current trip itinerary.
@booking_blueprint.route('/applied_jobs')
def booking_trip():

	db = Database().db
	cursor = db.cursor()
	query = get_jobs_applied()
	cursor.execute(query)
	jp = [dict(id = row[1], name=row[2], description=row[3],address= row[4],salary=row[5],status=row[7]) for row in cursor.fetchall()] # TODO: Correctly map activity info.
	# rows = cursor.fetchall()
	return render_template('applied_jobs.html',items=jp, session=session)
