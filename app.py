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



if __name__ == "__main__":
	app.debug = True
	app.run('127.0.0.1', 5000)
