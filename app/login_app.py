
# Import necessary libraries
import hashlib
from flask import Flask, flash, render_template, request, redirect, session, url_for, Blueprint
from src.customer import Customer
from src.database import Database

login_blueprint = Blueprint('login_blueprint', __name__)
dbOb= Database()
db = dbOb.db

def get_current_trip_id():
	return "select trip_id from trip natural join user where trip.is_booked=false and user.username='" + session['username'] + "';"


#####################################################################
#                        LOGIN / REGISTRATION                       #
#####################################################################

# Login/Registration Page. Redirects to home if already logged in.
@login_blueprint.route('/login-page')

def login_page():

	# Show login page if not logged in. Redirect to home if already logged in.
	if 'username' not in session or session['username'] == '':
		return render_template('login.html')
	else:
		return redirect(url_for('home'))

# On Login Form Submit. Loads home page or shows error.
@login_blueprint.route('/login', methods=['POST'])
def verify_credentials():

	# Parse user input fields
	name=request.form['login_username']
	password=hashlib.sha256(request.form['login_password'].encode('utf-8')).hexdigest()

	# Query Database
	db = Database().db
	cursor = db.cursor()
	cursor.execute("select * from user where username = '" + name + "' and password = '" + password + "';")
	rows = cursor.fetchall()
	error = None

	if rows:
		# User found
		if rows[0][7] != 1:
			# Not suspended
			session['username'] = rows[0][0]
			session['email'] = rows[0][2]
			session['is_admin'] = rows[0][3]
			session['name'] = rows[0][4]

			# Set current trip id for this user.
			query = get_current_trip_id()
			cursor.execute(query)
			trip_ids = cursor.fetchall()

			if len(trip_ids) > 0:
				# There are trips for this user. If no, just make it when they start adding attractions.
				session['current_trip_id'] = trip_ids[0][0]

			return redirect(url_for('home'))
		else:
			# Suspended user
			error='User suspended.'
	else:
		# No such user. Login again.
		error = 'Incorrect username or password. Please try again.'
	return render_template('login.html', error=error)

# Logs out of system and redirects to pictures.
@login_blueprint.route('/logout')
def logout():

	# Clear out session variables
	session.clear()
	return redirect(url_for('index'))

# On Register Form Submit. Loads home page.
# TODO: Re-fill out correct fields when registration fails.
@login_blueprint.route('/register', methods=['POST'])
def register():

	# Parse user input fields
	name=request.form['register_username']
	password1=hashlib.sha256(request.form['register_password'].encode('utf-8')).hexdigest()
	password2=hashlib.sha256(request.form['register_password2'].encode('utf-8')).hexdigest()
	firstname=request.form['register_firstname']
	lastname=request.form['register_lastname']
	email=request.form['register_email']
	street=request.form['register_streetaddress']
	city=request.form['register_city']
	state=request.form['register_state']
	country=request.form['register_country']
	zipcode=request.form['register_zip']
	customer_ob = Customer(name, password1,password2, email, firstname, lastname, street, city, state, country, zipcode)

	error = customer_ob.validate_data()
	if error != 0:
		return render_template('login.html', error2=error, scroll="register")
	insert_address_query,insert_username_query = customer_ob.create_query()
	dbOb.insert(insert_address_query)
	dbOb.insert(insert_username_query)

	# Update current user session
	session['username'] = name
	session['name'] = firstname
	session['is_admin'] = 0
	session['email'] = email

	return redirect(url_for('home'))


#####################################################################
#                             User                                  #
#####################################################################

@login_blueprint.route('/edit-user/<username>')
def edit_user(username):
    db = Database().db
    cursor = db.cursor()
    query = """SELECT u.username, u.email, u.is_admin, u.first_name, u.last_name, u.suspended,
            a.street_no, a.street_name, a.city, a.state, a.country, a.zip
            FROM user u
            JOIN address a ON u.address_id = a.address_id
            WHERE u.username = '{}'""".format(username)
    cursor.execute(query)
    data = cursor.fetchone()
    return render_template('edit-user.html', param=username, data=data)

@login_blueprint.route('/update-user', methods=['POST'])
async def update_user():
	# Parse user input fields
	name=request.form['register_username']
	firstname=request.form['register_firstname']
	lastname=request.form['register_lastname']
	email=request.form['register_email']
	street=request.form['register_streetaddress']
	city=request.form['register_city']
	state=request.form['register_state']
	country=request.form['register_country']
	zipcode=request.form['register_zip']
	customer_ob = Customer(name, "","", email, firstname, lastname, street, city, state, country, zipcode)

	# Get Address ID
	db = Database().db
	cursor = db.cursor()
	cursor.execute("select address_id from user where username='" + name + "';")
	address_id = cursor.fetchall()[0][0]
 
	print(address_id)
	cursor.execute("select * from address where address_id='" + str(address_id) + "';")
	data=cursor.fetchall()
	print(data)
	error = customer_ob.validate_data_for_update()
	if error != 0:
		return render_template('edit-user.html',param=name,
                         data=(name, email, False, firstname, lastname, False, "", "", city, state, country, zipcode)
                         , error2=error)
	address_query, address_values, user_query, user_values = customer_ob.update(address_id)
	dbOb.execute_with_values(address_query, address_values)
	dbOb.execute_with_values(user_query, user_values)
	cursor.execute("select * from address where address_id='" + str(address_id) + "';")
	data=cursor.fetchall()
	return redirect(url_for('home'))


