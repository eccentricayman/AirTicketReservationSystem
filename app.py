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
		departureAirport = request.form.get('departureAirport')
		arrivalAirport = request.form.get('arrivalAirport')
		departureDate = request.form.get('departureDate')
		arrivalDate = request.form.get('arrivalDate')
		if (departureAirport == arrivalAirport == departureDate == arrivalDate == ""):
			flash("Enter at least one value.")
			return redirect(url_for("search"))
		else:
			query = "SELECT * FROM flights WHERE "
			inserts = []
			if departureAirport != "":
				query += "departureAirport = %s AND "
				inserts.append(departureAirport)
			if arrivalAirport != "":
				query += "arrivalAirport = %s AND "	
				inserts.append(arrivalAirport)
			if departureDate != "":
				query += "departureDateTime = %s AND "
				x = datetime.strptime(departureDate, '%Y-%m-%d')
				inserts.append(x)
			if arrivalDate != "":
				query += "arrivalDateTime = %s AND "	
				inserts.append(arrivalDate)	
			query = query[:-4]
			print(query)
			cursor = db.cursor()
			cursor.execute(query, tuple(inserts))
			data = cursor.fetchall()
			return render_template("search.html", data = data)
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
			return redirect(url_for('customerHome'))
		elif (airlineData):
			session['username'] = username
			session['user_type'] = 'AirlineStaff'
			return redirect(url_for('staffHome'))
		else:
			flash("Invalid login or username")
			return render_template('login.html')
	else:
		return render_template('login.html')

@app.route('/customerHome', methods=['GET','POST'])
def customerHome():
	return render_template('customerHome.html')

@app.route('/staffHome', methods=['GET','POST'])
def staffHome():
	return render_template('staffHome.html')

@app.route("/viewFlights", methods=["GET", "POST"])
def viewFlights():
	cursor = db.cursor()
	customerQuery = 'SELECT DISTINCT f.* from Ticket t join Flights f on t.flightNumber = f.flightNumber where customerEmail = %s and departureDateTime >= now()'
	cursor.execute(customerQuery, (session['username']))
	customerFlights = cursor.fetchall()
	#A display results to users 
	for item in customerFlights:
		print(item)
	return render_template('customerHome.html')

@app.route("/purchaseTickets", methods=["GET", "POST"])
def purchaseTickets():
	if request.method == "POST":
		cursor = db.cursor()
		#check if full check flights - airplaneId check number of seats 
		flightNumber = request.form['flightNumber']
		creditOrDebit = request.form['creditOrDebit']
		cardNumber = request.form['cardNumber']
		NameOnCard = request.form['NameOnCard']
		cardExp = request.form['cardExp']

		numSeatsQuery = 'SELECT a.seats, f.basePrice, f.airline from Flights f join Airplane a on a.airplaneId = f.airplaneId f.flightNumber = %s'
		cursor.execute(numSeatsQuery, (flightNumber))
		#A get the results of the query and store into NumSeats, BasePrice, airlineName (rn have dummy values of 1 n empty string)
		numSeats = 1
		basePrice = 1
		airlineName = ""
		if (numSeats == 0):
			flash("No More Seats Avail")
			return redirect(url_for("purchaseTicket"))
		elif (numSeats < 15):
			basePrice = basePrice*1.15
		#insert into ticket table + get credit card info 
		purchaseTicketQuery = 'INSERT into Tickets VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute("SELECT NOW();")
		timeRN = cursor.fetchone()
		cursor.execute(purchaseTicketQuery, (str(numSeats), session['username'],airlineName,flightNumber,str(basePrice),str(timeRN),creditOrDebit,cardNumber,NameOnCard,cardExp))
		db.commit()
		cursor.close()
		return redirect(url_for('purchaseTicket'))
	else:
		return render_template('purchaseTicket.html')

@app.route("/trackSpending", methods=["GET", "POST"])
def trackSpending():
	cursor = db.cursor()
	#look at Ticket table n add up for the user (done) for the past year 
	#a bar chart/table showing month wise money spent for last 6 months CURDATE() - INTERVAL 6 MONTH;
	#option to specify a range of dates and look at charts for specified time 
	spendingQuery = 'Select sum(soldPrice) from Ticket where customerEmail = %s and purchaseDateTime > dateadd(year, -1, now())'
	cursor.execute(spendingQuery, (session['username']))
	spendingSixMonthsQuery = ''
	return render_template('customerHome.html')

@app.route("/rate", methods=["GET", "POST"])
def rate():
	#check if the user previously took the flight - ask for flight number in Tickets db 
	#insert their rating into table ViewPreviousFlights? 
	if request.method == "POST":
		flightNumber = request.form['flightNumber']
		rate = request.form['rate']
		comment = request.form['comment']
		cursor = db.cursor()
		checkFlightQuery = 'SELECT ticketID from Ticket where flightNumber = %s and customerEmail = %s'
		cursor.execute(checkFlightQuery, (flightNumber,session['username']))
		customerTicket = cursor.fetchone()
		if (customerTicket is None):
			flash("User didn't take flight")
			return redirect(url_for('rate'))
		else:
			ins = 'INSERT INTO ViewPreviousFlights VALUES(%s, %s, %s, %s)'
			cursor.execute(ins, (session['username'],flightNumber,rate,comment))
			db.commit()
			cursor.close()
			return redirect(url_for('rate'))
	else:
		return render_template('rateFlight.html')


	


@app.route("/logout", methods=["GET", "POST"])
def logout():
	del session['username']
	del session['user_type']
	return redirect(url_for(index))


if __name__ == "__main__":
	app.debug = True
	app.run()
