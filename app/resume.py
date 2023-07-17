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
        # return redirect(binary_pdf)
        # with open(binary_pdf, 'rb') as static_file:
        #       return send_file(static_file, session['username']+".pdf")
        print(binary_pdf)
        response = make_response(binary_pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=%s' % binary_pdf
        return response
		
db = Database().db

# Shows all available attractions.
@resume_blueprint.route('/resume')
def view_resume():
	return render_template('resume.html', session=session)

