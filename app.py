from flask import Flask, render_template, request, session, url_for, redirect
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
		
	else:
		return render_template("search.html")

#Define route for register
@app.route('/register', methods=['GET','POST'])
def register():
	if request.method == "POST":
		#grabs information from the forms
		username = request.form['username']
		password = request.form['password']

		cursor = db.cursor()
		error = None

		customerQuery = 'SELECT * FROM Customer WHERE email = %s'
		cursor.execute(customerQuery, (username))
		customerData = cursor.fetchone()

		airlineQuery = 'SELECT * FROM AirlineStaff WHERE username = %s'
		cursor.execute(airlineQuery, (username))
		airlineData = cursor.fetchone()
		
		if(customerData or airlineData):
			#If the previous query returns data, then user exists
			error = "This user already exists"
			return render_template('register.html', error = error)
		else:
			ins = 'INSERT INTO user VALUES(%s, %s)'
			cursor.execute(ins, (username, password))
			db.commit()
			cursor.close()
			return render_template('index.html')
	else: 
		return render_template('register.html')

#Define route for login
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == "POST":
		#grabs information from the forms
		username = request.form['username']
		password = request.form['password']

		cursor = db.cursor()
		error = None

		customerQuery = 'SELECT * FROM Customer WHERE email = %s and password = %s'
		cursor.execute(customerQuery, (username, password))
		customerData = cursor.fetchone()

		airlineQuery = 'SELECT * FROM AirlineStaff WHERE username = %s and password = %s'
		cursor.execute(airlineQuery, (username, password))
		airlineData = cursor.fetchone()

		cursor.close()
		
		if (customerData):
			session['username'] = username
			session['user'] = 'Customer'
			return redirect(url_for('home'))
		elif (airlineData):
			session['username'] = username
			session['user'] = 'AirlineStaff'
			return redirect(url_for('home'))
		else:
			error = 'Invalid login or username'
			return render_template('login.html', error=error)
	else:
		return render_template('login.html')




if __name__ == "__main__":
	app.debug = True
	app.run('127.0.0.1', 5000)