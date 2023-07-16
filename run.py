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
	