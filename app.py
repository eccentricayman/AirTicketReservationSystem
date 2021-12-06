from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import os
from init import *

app = Flask(__name__)
app.secret_key = os.urandom(32)

db = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor,)

#setup database
init()
db.select_db('AirTicketSystem')

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
	if request.method == "POST":
		sourceCity = request.form.get('sourceCity')
		sourceAirport = request.form.get('sourceAirport')
		destinationCity = request.form.get('destinationCity')
		destinationAirport = request.form.get('destinationAirport')
		departureDate = request.form.get('departureDate')
		arrivalDate = request.form.get('departureDate')
		if (sourceCity == sourceAirport == destinationAirport == destinationCity == departureDate == arrivalDate == ""):
			flash("Enter at least one value.")
			return render_template("search.html")
		#else:
			
	else:
		return render_template("search.html")

#Define route for register
@app.route('/register', methods=['GET','POST'])
def register():
	return render_template('register.html')

@app.route("/registerCustomer", methods=["GET", "POST"])
def registerCustomer():
	if request.method == "POST":
		email = request.form['email']
		password = request.form['password']
		password2 = request.form['password2']

		if (password != password2):
			flash("Passwords don't match")
			return redirect(url_for("registerCustomer"))
		
		name = request.form['name']
		buildingNum = request.form['buildingNum']
		street = request.form['street']
		city = request.form['city']
		state = request.form['state']
		PhoneNumber = request.form['PhoneNumber']
		PassportNumber = request.form['PassportNumber']
		passportExDate = request.form['passportExDate']
		dob = request.form['dob']
		passportCountry = request.form['passportCountry']

		#print(name,buildingNum,street,city,state,PhoneNumber,PassportNumber,passportExDate,dob,passportCountry)

		cursor = db.cursor()
		error = None

		customerQuery = 'SELECT * FROM Customer WHERE email = %s'
		cursor.execute(customerQuery, (email))
		customerData = cursor.fetchone()
		print(customerData)
		if(customerData):
			flash("This user already exists")
			return redirect(url_for("registerCustomer"))
		else:
			ins = 'INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
			cursor.execute(ins, (name,email, password,buildingNum,street,city,state,PhoneNumber,PassportNumber,passportExDate,dob,passportCountry))
			db.commit()
			cursor.close()
			return redirect(url_for("index"))
	else:
		return render_template("registerCustomer.html")

@app.route("/registerStaff", methods=["GET", "POST"])
def registerStaff():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		password2 = request.form['password2']

		if (password != password2):
			flash("Passwords don't match")
			return redirect(url_for("registerCustomer"))

		firstName = request.form['firstName']
		lastName = request.form['lastName']
		dob = request.form['dob']
		phoneNumber = request.form['PhoneNumber']
		airline = request.form['Airline']

		#print(firstName,lastName,dob,phoneNumber,airline)
		
		cursor = db.cursor()
		error = None

		airlineQuery = 'SELECT * FROM AirlineStaff WHERE username = %s'
		cursor.execute(airlineQuery, (username))
		airlineData = cursor.fetchone()
		
		if(airlineData):
			flash("This user already exists")
			return redirect(url_for("registerStaff"))
		else:
			ins = 'INSERT INTO AirlineStaff VALUES(%s, %s, %s, %s, %s, %s, %s)'
			cursor.execute(ins, (username, password,firstName,lastName,dob,phoneNumber,airline))
			db.commit()
			cursor.close()
			return redirect(url_for('index'))
	else:
		return render_template("registerStaff.html")


#Define route for login
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == "POST":
		#grabs information from the forms
		username = request.form['username']
		password = request.form['password']
		password2 = request.form['password2']

		if (password != password2):
			flash("Passwords don't match")
			return render_template('login.html')

		cursor = db.cursor()
		error = None

		customerQuery = 'SELECT * FROM Customer WHERE email = %s and password = %s'
		cursor.execute(customerQuery, (username, password))
		customerData = cursor.fetchone()

		airlineQuery = 'SELECT * FROM AirlineStaff WHERE username = %s and password = %s'
		cursor.execute(airlineQuery, (username, password))
		airlineData = cursor.fetchone()

		debugQuery = 'SELECT * from Customer'
		cursor.execute(debugQuery)
		print(cursor.fetchone())

		cursor.close()
		
		if (customerData):
			session['username'] = username
			session['user_type'] = 'Customer'
			return redirect(url_for('home'))
		elif (airlineData):
			session['username'] = username
			session['user_type'] = 'AirlineStaff'
			return redirect(url_for('home'))
		else:
			flash("Invalid login or username")
			return render_template('login.html')
	else:
		return render_template('login.html')




if __name__ == "__main__":
	app.debug = True
	app.run()
