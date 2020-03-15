from flask import Flask, session, request, Response, g, redirect, url_for, abort, render_template, flash, make_response
from src.mastermind import Mastermind
from var_dump import var_dump

app = Flask(__name__)
app.debug = True
app.secret_key = b'\x17\xc7#\x94\xfa&\xd5\xff\xec\x9f1\xb5\xe4\nv\xf7'

mastermind = Mastermind()

def startUp():
    if 'name' in session:
        mastermind.playerName = session['playerName']
        mastermind.started = True

@app.route('/')
def hello_world():
    return render_template('welcome.html');

@app.route('/playername', methods=['POST'])
def playerName():
    mastermind.playerName = request.form['playerName']
    mastermind.doubleColors = False
    mastermind.generate()
    mastermind.save()
    return render_template('welcome.html')
