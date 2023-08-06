from flask import Flask, flash, render_template, request, redirect, session, url_for, Blueprint
import os
from src.database import Database
from flask import make_response,send_from_directory, send_file, current_app as app
resume_blueprint = Blueprint('resume_blueprint', __name__ )
#####################################################################
#                             Flights                               #
#####################################################################
def get_trip_cost():
	return "select sum(price) from trip_common  where username=\"" + (session['username']) + "\"and is_booked = false;"

def get_all_activities_in_a_trip():
	# return "select activity_date, activity_name, cost, activity_start_time, activity_end_time, activity_id from activity natural join trip where username = '" + session['username'] + "' and is_booked = false;"
	return "select * from trip_common where username = '" + session['username'] + "' and is_booked = false;";



UPLOAD_FOLDER = '/Users/ashu/visualStudio/SOEN 6011/Career-Planner-master/resume'
ALLOWED_EXTENSIONS = set(['pdf'])
# resume_blueprint.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@resume_blueprint.route('/edit-user/<username>')
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


@resume_blueprint.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'pdf-file' not in request.files:
            flash('No pdf file')
        pdf_file = request.files['pdf-file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if pdf_file.filename == '':
            flash('No pdf file selected')
            return redirect(request.url)
        if pdf_file and allowed_file(pdf_file.filename):
            filename = session['username']+".pdf"
            pdf_file.save(os.path.join(UPLOAD_FOLDER , filename))
    return render_template('resume.html')

@resume_blueprint.route('/docs/<id>')
def show_pdf(id=None):
    print("id-----------------------------------",id)
    if id is not None:
        binary_pdf = UPLOAD_FOLDER+"/"+id+".pdf"
        return send_from_directory(UPLOAD_FOLDER, id+".pdf")
		
db = Database().db

# Shows all available attractions.
@resume_blueprint.route('/resume')
def view_resume():
    db = Database().db
    cursor = db.cursor()
    query = """SELECT * from skills
            WHERE username = '{}'""".format(session["username"])
    cursor.execute(query)
    data = cursor.fetchone()
    return render_template('resume.html', session=session,data=data)


@resume_blueprint.route('/update-skill', methods=['POST'])
def update_skills():
    db = Database().db
    cursor = db.cursor()
    username = session["username"]
    skill=request.form['skill']
    firstname=request.form['register_firstname']
    lastname=request.form['register_lastname']
    email=request.form['register_email']

    query1= "INSERT INTO skills (username, skills,first_name,last_name,email_address) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE skills = %s"
    query = """insert
            WHERE username = '{}'""".format(session["username"])
    values = (username,skill,firstname,lastname,email,skill)
    cursor.execute(query1,values)
    db.commit()
    return redirect("/resume")
