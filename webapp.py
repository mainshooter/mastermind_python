from flask import Flask, session, request, Response, g, redirect, url_for, abort, render_template, flash, make_response

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('welcome.html');
