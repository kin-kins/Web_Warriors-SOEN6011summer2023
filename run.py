
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
import app.jobs_posting  as jobs_app
import app.login_app as login_app
import app.applied_jobs as applied_app

app = Flask(__name__)
app.config['SECRET_KEY'] = '8ffe05624dfe0efdf7c7f67288d4f4ce5005e0dfb6a1bc48366ef9906dd0586e'
app.register_blueprint(resume_app.resume_blueprint, url_prefix='/')
app.register_blueprint(jobs_app.job_blueprint, url_prefix='/')
app.register_blueprint(login_app.login_blueprint, url_prefix='/')
app.register_blueprint(applied_app.booking_blueprint, url_prefix='/')
dbOb= Database()



#####################################################################
#                          SQL Queries                              #
#####################################################################

def get_jp_data():
	db = Database().db
	cursor = db.cursor()
	cursor.execute("select * from job_posting;")
	jp = [dict(name=row[1], description=row[2], address=row[3],salary=row[4]) for row in cursor.fetchall()]
	return jp

#####################################################################
#                         INDEX/HOME                                #
#####################################################################

def list_page(no_error):

	# Query database when user is admin for admin panel
	if session['is_admin']:

		# Get user table information.
		db = Database().db
		cursor = db.cursor()
		cursor.execute("select * from user;")
		users = [dict(is_admin="Yes" if row[3] == 1 else "No", username=row[0], password=row[1], first_name=row[4], last_name=row[5], email=row[2], suspended="Yes" if row[7] == 1 else "No") for row in cursor.fetchall()]

		if no_error:
			return render_template("home.html", session=session, users=users)
		else:
			return render_template("home.html", session=session, users=users)

	# Not an admin
	if no_error:
		if 'current_trip_id' not in session or not session['current_trip_id']:
			return render_template("home.html", session=session)
		return render_template("home.html", session=session)
	else:
		return render_template("home.html", session=session)


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
	return list_page(no_error=True)

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

@app.route('/notifications')
def notifications():
	db = Database().db
	cursor = db.cursor()
	cursor.execute(f"select * from notifications where username= '{session['username']}' and seen=0;")
	db.commit()
	item = [dict(keyid=row[0],alert = row[2]) for row in cursor.fetchall()] 
	# cursor.execute("update user set is_admin=1 where username='" + username + "';")
	cursor.execute(f"update notifications set seen=1 where username= '{session['username']}' and seen=0;")
	db.commit()
	return render_template('notifications.html',session=session,items=item)

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



@app.route('/review-candidate/<jp_id>/<jp_username>', methods=['POST'])
def review_candidate(jp_id,jp_username):
	db = Database().db
	cursor = db.cursor()
	print("update job_applied set status='Review' where applied_job_id="+jp_id+ " ;")
	cursor.execute("update job_applied set status='Review' where applied_job_id="+jp_id+ " ;")
	db.commit()
	return render_template('resume.html',username=jp_username, session=session)


@app.route('/approve-candidate/<jp_id>/<jp_username>/<jobid>', methods=['POST'])
def approve_candidate(jp_id,jp_username,jobid):
	db = Database().db
	cursor = db.cursor()
	cursor.execute("update job_applied set status='Approved' where applied_job_id="+jp_id+ " ;")
	db.commit()
	return redirect('/review-jobs/'+jobid, code=307)



@app.route('/decline-candidate/<jp_id>/<jp_username>/<jobid>', methods=['POST'])
def decline_candidate(jp_id,jp_username,jobid):
	db = Database().db
	cursor = db.cursor()
	cursor.execute("update job_applied set status='Declined' where applied_job_id="+jp_id+ " ;")
	db.commit()
	return redirect('/review-jobs/'+jobid, code=307)



#####################################################################
#                         MAIN APPLICATION                          #
#####################################################################

# Run the application
if __name__ == '__main__':
	db = Database().get_db()
	# Note: If your database uses a different password, enter it here.
	app.run(debug=True, host='0.0.0.0', port=8000)
	