from src.activity import Activity
from flask import Flask, flash, render_template, request, redirect, session, url_for, Blueprint

from src.database import Database
job_blueprint = Blueprint('activities_blueprint', __name__)
db = Database().db

def get_jp_data():
	db = Database().db
	cursor = db.cursor()
	if int(session["is_admin"]) == 2:
		cursor.execute("select * from job_posting where company_name=\'"+ session['username']+ "';" )
		# "select trip_id from trip natural join user where trip.is_booked=false and user.username='" + session['username'] + "';"
	else:
		cursor.execute("select * from job_posting;")
	jp = [dict(jobid = row[0],name=row[1], description=row[2], address=row[3],salary=row[4]) for row in cursor.fetchall()]
	return jp

#####################################################################
#                        Activities                                 #
#####################################################################

def get_jobs_applied():
	# return "select activity_date, activity_name, cost, activity_start_time, activity_end_time, activity_id from activity natural join trip where username = '" + session['username'] + "' and is_booked = false;"
	return "select * from job_applied where username = '" + session['username'] + "';"
 


# Shows all available attractions.
@job_blueprint.route('/jobs')
def attractions():
	jp = get_jp_data()
	return render_template('jobs.html', items=jp, session=session)

# Receive attraction data to turn into an activity
@job_blueprint.route('/add-to-jobs/<jp_index>', methods=['POST'])
def add_to_trip(jp_index):
	cursor = db.cursor()
	cursor.execute("select * from job_posting;")
	jp = [dict(id = row[0], name=row[1], description=row[2],address= row[3],salary=row[4]) for row in cursor.fetchall()] # TODO: Correctly map activity info.
	jobid = jp[int(jp_index) - 1]['id']
	description = jp[int(jp_index) - 1]['description']
	name = jp[int(jp_index) - 1]['name']
	price = jp[int(jp_index) - 1]['salary']
	address = jp[int(jp_index) - 1]['address']
	values = (jobid,name,description,price,address, session['username'])
	query_trip_common = "INSERT IGNORE INTO job_applied ( job_id, company_name ,description,salary,address, username) VALUES (%s, %s, %s, %s, %s,%s)"
	print(query_trip_common,values)
	cursor.execute(query_trip_common, values)
	query = get_jobs_applied()
	cursor.execute(query)
	db.commit()
	jp = [dict(id = row[1], name=row[2], description=row[3],address= row[4],salary=row[5]) for row in cursor.fetchall()] # TODO: Correctly map activity info.
	# print(jp)
	return render_template('applied_jobs.html',items=jp, session=session)



# Delete an attraction
@job_blueprint.route('/delete-jobs/<jp_index>', methods=['POST'])
def delete_jobs(jp_index):
	print("job posting ----------",jp_index)
	# Get attraction_name
	db = Database().db
	cursor = db.cursor()
	cursor.execute("delete from job_posting where job_id= " + jp_index + ";")
	db.commit()
	return redirect('/jobs')


@job_blueprint.route('/review-jobs/<jp_index>', methods=['POST'])
def review_jobs(jp_index):
	print("Review posting ----------",jp_index)
	# Get attraction_name
	db = Database().db
	cursor = db.cursor()
	cursor.execute("select * from job_applied where job_id= " + jp_index + ";")
	db.commit()
	jp = [dict(keyid=row[0],id = row[1], name=row[2], description=row[3],address= row[4],salary=row[5],username= row[6],status=row[7]) for row in cursor.fetchall()] # TODO: Correctly map activity info.
	
	return render_template('review_candidate.html',items=jp,jobid=jp_index, session=session)


@job_blueprint.route('/review-candidate/<jp_id>/<jp_username>', methods=['POST'])
def review_candidate(jp_id,jp_username):
	db = Database().db
	cursor = db.cursor()
	print("update job_applied set status='Review' where applied_job_id="+jp_id+ " ;")
	cursor.execute("update job_applied set status='Review' where applied_job_id="+jp_id+ " ;")
	db.commit()
	return render_template('resume.html',username=jp_username, session=session)


@job_blueprint.route('/approve-candidate/<jp_id>/<jp_username>/<jobid>', methods=['POST'])
def approve_candidate(jp_id,jp_username,jobid):
	db = Database().db
	cursor = db.cursor()
	cursor.execute("update job_applied set status='Approved' where applied_job_id="+jp_id+ " ;")
	db.commit()
	return redirect('/review-jobs/'+jobid, code=307)



@job_blueprint.route('/decline-candidate/<jp_id>/<jp_username>/<jobid>', methods=['POST'])
def decline_candidate(jp_id,jp_username,jobid):
	db = Database().db
	cursor = db.cursor()
	cursor.execute("update job_applied set status='Declined' where applied_job_id="+jp_id+ " ;")
	db.commit()
	return redirect('/review-jobs/'+jobid, code=307)


@job_blueprint.route('/add-activity', methods=['GET'])
def add_activityt():
	return render_template('add_activity.html')

@job_blueprint.route('/activity-create', methods=['POST'])
def create_activitys():
    
	if request.method == 'POST':
		activity_name = session['username']
		activity_desc = request.form['activity_desc']
		activity_address = request.form['activity_address']
		price = request.form['price']
		activity_object = Activity(activity_name, activity_desc, activity_address,price)
		activity_object.save()
		return redirect('/jobs')
	return redirect('/jobs')