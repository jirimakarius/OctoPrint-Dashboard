from flask import Flask, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = "something"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
import octoprint_dashboard.model

import octoprint_dashboard.cli_commands

import octoprint_dashboard.login.routes
import octoprint_dashboard.api



@app.route('/')
def frontend():
    # return "Hello"
    # return render_template('index.html')
    return send_from_directory('dist', 'index.html')


@app.route('/<text>.js')
def neco(text):
    return send_from_directory('dist', text + ".js")





@app.route('/api/upload', methods=['PUT'])
def upload():
    print(request.data)
    for i in request.files.keys():
        print(i)
    return 'parek', 201

