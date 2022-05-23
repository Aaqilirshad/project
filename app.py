import os
from cs50 import SQL
from flask import flask_session, Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

#configure application
app = Flask(__name__)

#make sure templates are auto reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
