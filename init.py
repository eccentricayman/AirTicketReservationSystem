import pymysql.cursors

def init():
	db = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor,)

	cursor = db.cursor()


	cursor.execute('CREATE DATABASE if not exists AirTicketSystem;')
	db.select_db('AirTicketSystem')
	db.commit()

	query = '''
		CREATE TABLE if not exists Customer (
			name varchar(50),
			email varchar(50),
			password varchar(50),
			buildingNumber bigint,
			street varchar(50),
			city varchar(50),
			state varchar(50),
			phoneNumber varchar(50),
			passportNumber varchar(50),
			passportExpiration date,
			dateOfBirth date,
			passportCountry varchar(50)
		);

		CREATE TABLE if not exists Ticket (
			ticketID varchar(30),
			customerEmail varchar(50),
			airlineName varchar(50),
			flightNumber varchar(50),
			soldPrice bigint,
			purchaseDateTime datetime,
			creditOrDebit boolean,
			cardNumber varchar(20),
			nameOnCard varchar(50),
			cardExpirationDate varchar(20)
		);

		CREATE TABLE if not exists CheckSeats (
			ticketID varchar(30),
			airplaneID varchar(30),
			adjustedPrice NUMERIC(10,5)
		);

		CREATE TABLE if not exists ViewPreviousFlights (
			email varchar(50),
			flightNumber varchar(50),
			departureDateTime datetime,
			rate int,
			comment varchar(200)
		);

		CREATE TABLE if not exists ViewFutureFlights (
			email varchar(50),
			flightNumber varchar(50),
			rate int,
			comment varchar(200)
		);

		CREATE TABLE if not exists Purchase (
			ticketID varchar(30),
			email varchar(50)
		);

		CREATE TABLE if not exists Airline (
			name varchar(50)
		);

		CREATE TABLE if not exists Airplane (
			airplaneId varchar(50),
			seats int,
			airline varchar(30)
		);

		CREATE TABLE if not exists AddAirplane (
			airplaneId varchar(50),
			username varchar(40)
		);

		CREATE TABLE if not exists AirlineStaff (
			username varchar(40),
			password varchar(30),
			firstName varchar(30),
			lastName varchar(30),
			dateOfBirth date,
			phoneNumber varchar(30),
			airline varchar(30)
		);

		CREATE TABLE if not exists ViewFlight (
			username varchar(40),
			password varchar(30),
			firstName varchar(30),
			lastName varchar(30),
			dateOfBirth date,
			phoneNumber varchar(30),
			airline varchar(30)
		);


		CREATE TABLE if not exists Flights (
			flightNumber varchar(50),
			departureDateTime datetime,
			airline varchar(30),
			arrivalAirport varchar(30),
			basePrice NUMERIC(10,5),
			arrivalDateTime datetime,
			departureAirport varchar(30),
			airplaneId varchar(50)
		);

		CREATE TABLE if not exists FlightStatus (
			flightNumber varchar(50),
			departureDateTime datetime,
			username varchar(50),
			status varchar(30)
		);


		CREATE TABLE if not exists Operates (
			name varchar(50),
			flightNumber varchar(50),
			departureDateTime datetime
		);


		CREATE TABLE if not exists Airport (
			airportID int,
			name varchar(30),
			city varchar(30)
		);

		CREATE TABLE if not exists Departs (
			flightNumber varchar(50),
			departureDateTime datetime,
			airportID int
		);


		CREATE TABLE if not exists Arrives (
			flightNumber varchar(50),
			departureDateTime datetime,
			airportID int
		);
	'''
	queries = query.split(";")
	for query in queries[:-1]:
		cursor.execute(query)