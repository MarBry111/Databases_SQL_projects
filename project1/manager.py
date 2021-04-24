import os

from flask import Flask
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy

import urllib


app = Flask(__name__)

params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=localhost;DATABASE=homerowk1;Trusted_Connection=yes;')
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params

db = SQLAlchemy(app)