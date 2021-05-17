from flask import Flask, render_template, redirect, flask, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db

app = Flask(__name__)
