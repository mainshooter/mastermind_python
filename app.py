from flask import Flask, session, request, Response, g, redirect, url_for, abort, render_template, flash, make_response
from src.mastermind import Mastermind, Database
from var_dump import var_dump

app = Flask(__name__)
app.debug = True
app.secret_key = b'\x17\xc7#\x94\xfa&\xd5\xff\xec\x9f1\xb5\xe4\nv\xf7'

mastermind = Mastermind()

def startUp():
    if 'playerName' in session:
        mastermind.playerName = session['playerName']
        mastermind.solutionColors = session['solutionColors']
        mastermind.gameFinisht = session['gameFinisht']
        mastermind.playerAnswerJsonToObject(session['playerAnswers'])
        mastermind.started = True
        mastermind.doubleColors = session['doubleColors']

@app.route('/')
def index():
    startUp()
    if mastermind.canPlay() is True:
        return redirect(url_for('playRound'))
    return render_template('welcome.html');

@app.route('/playername', methods=['POST'])
def playerName():
    startUp()
    mastermind.playerName = request.form['playerName']
    if 'doubleColors' in request.form:
        mastermind.doubleColors = bool(request.form['doubleColors'])
    else:
        mastermind.doubleColors = False
    mastermind.generate()
    mastermind.started = True
    mastermind.save()
    return redirect(url_for('playRound'))

@app.route('/game', methods=['GET'])
def playRound():
    startUp()
    if mastermind.canPlay() is False:
        return redirect(url_for('index'))
    return render_template('game.html', game=mastermind)

@app.route('/game-post', methods=['POST'])
def handleRound():
    startUp()
    givenAnswers = request.form.getlist('color[]')
    mastermind.handleAnswers(givenAnswers)
    mastermind.isFinisht()
    mastermind.save()
    if (mastermind.gameFinisht == True):
        mastermind.saveToDb()
        session.clear()
        return render_template('done.html', game=mastermind)
    else:
        return redirect(url_for('playRound'))

@app.route('/stats')
def stats():
    db = Database()
    rows = db.query("SELECT * FROM players ORDER BY id DESC")
    db.close()
    return render_template("stats.html", rows=rows);
