from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, RadioField
from random import Random
import cv2, numpy
from werkzeug import secure_filename
from flask_wtf.file import FileField
from analyzeimage import analyzeimage
from PIL import Image
import time
import urllib.request
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, Response, send_file
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2e278443e'
app.config['UPLOAD_FOLDER'] = 'uploads/'

# # import a python file from a different folder - this will be done later
# import sys
# sys.path.insert(0, "access-images/")
# from RemoteSensingDB import RemSensDB

class ReusableForm(Form):
	### Define text fields and other inputs for the forms on both html pages
	indexfortemps = 0
	error = ""
	radio = RadioField("Search by", choices=[("File", "File"), ("Name","Name"),("ID","ID")], default="Name")
	name = TextField("Filename", description="filename")
	id_number = TextField("Filename", description="id number")
	file = FileField(u'Image File')

	# app.route(path) is the python function run at localhost:8484/path
	# the '@' symbol is a decorator function
	# when 'app.route' (a function) is run with the arguments below
	# python also runs 'imagepage'
	# the arguments of 'imagepage' are the outputs of the decorated function
	@app.route("/analyze/<string:imname>", methods=['GET', 'POST'])
	def imagepage(imname):
		### these are the sources of the old (left) and new (right) images
		old_image = "/static/{}.jpg".format(imname)
		# before analysis, both images have the same source (and are identical)
		new_image = old_image

		# create a form
		form = ReusableForm(request.form)

		# this runs when the form is submitted
		# and the website gets the data as a POST request
		# more on POST (and GET) requests at https://developer.mozilla.org/en-US/docs/Learn/HTML/Forms/Sending_and_retrieving_form_data
		if request.method == 'POST':
			print("old_image", old_image)
			# remove initial "/" from the image src so the computer can access it
			filename_of_image_to_analyze = old_image[1:]
			##################################################################################################
			# analyze the image, and write it to static/temp.jpg (NO STARTING SLASH)
			new_image = analyze_image(filename_of_image_to_analyze)
			# 
			##################################################################################################
			new_image = "/static/temp.jpg"
			print("new image", new_image)
			render_template('image.html', form=form, old_image=old_image, new_image=new_image)
			
		if form.validate():
			# if all required fields are submitted, this returns true
			pass

		# add the current time to the end of the filename to prevent computers from caching images
		old_image_time = "{}?time={}".format(old_image,time.time())
		new_image_time = "{}?time={}".format(new_image,time.time())
		
		return render_template('image.html', form=form, old_image=old_image_time, new_image=new_image_time)

	@app.route("/", methods=['GET','POST'])
	def query():
		# create RemSensDB object (defined in RemoteSensingDB.py)
		dataset = RemSensDB()
		# create form
		form = ReusableForm(request.form)

		if request.method == "POST":
			"""
			process data
			if we find an error in filling out the form, it will print to the console
			"""
			try:
				searchType = request.form["radio"]
				if searchType == "Name":
					# if searching by name
					filename = request.form["name"]
					if not filename:
						raise AssertionError("Missing filename")
					# acquire this file from the database
					filestr = dataset.findByName(filename)
					if not filestr:
						raise AssertionError("Image not found")
					# convert db buffer image to a numpy array
					npimg = numpy.frombuffer(filestr, numpy.uint8)
					# convert numpy image to an opencv image
					img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
					# save the image to static/analyze.jpg for accessing later
					cv2.imwrite("static/analyze.jpg",img)
					
				elif searchType == "ID":
					# if searching by ID
					id_number = request.form["id_number"]
					if not id_number:
						raise AssertionError("Missing ID")
					# acquire this file from the database
					filestr = dataset.findByID(id_number)
					if not filestr:
						raise AssertionError("Image not found")
					# convert db buffer image to a numpy array
					npimg = numpy.frombuffer(filestr, numpy.uint8)
					# convert numpy image to an opencv image
					img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
					# save the image to static/analyze.jpg for accessing later
					cv2.imwrite("static/analyze.jpg",img)

				elif searchType == "File":
					# if uploading an image
					# get the uploaded file
					uploadFilename = request.files['file']
					if not uploadFilename:
						raise AssertionError("Missing File")
					# save the image to static/analyze.jpg for accessing later
					uploadFilename.save("static/analyze.jpg")
					
			except AssertionError as e:
				print("\n\n\n\n\n\n~~~~~\n{}\n~~~~~\n\n\n\n".format(e))
			# redirect to the analysis page
			return redirect(url_for('imagepage', imname="analyze"))
		return render_template('query.html', form=form)


	# @app.route("/browse/<int:start>")
	# def browse(start):
	# 	return str(start)

# run the flask app at localhost:port
# go to localhost:8484 when running this code to see the project
def runFlask():
	app.run(port=8484, debug=True)

# if the program is being run, and not imported
if __name__ == "__main__":
	runFlask()