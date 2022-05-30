import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology, usd
from flask_mail import Mail, Message


#configure application
app = Flask(__name__)

#make sure templates are auto reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#comfigure app to use flask-mail
app.config["MAIL_SERVER"] = 'mail.gmx.com'
app.config["MAIL_PORT"] = 25
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'e-store@gmx.com'
app.config["MAIL_PASSWORD"] = 'icecream18106'
app.config["MAIL_DEFAULT_SENDER"] = 'e-store@gmx.com'
app.config["MAIL_ASCII_ATTACHMENTS"] = False

mail = Mail(app)


#filter
app.jinja_env.filters["usd"] = usd

db = SQL("sqlite:///shopper.db")

categories = [
    "Automotive",
    "Clothing&Fashion",
    "Computers",
    "Electronics",
    "Entertainment&Arts",
    "Health&Beauty",
    "Home&Garden",
    "Office&Professional",
    "Software",
    "Sports&Outdoors",
    "Stationaries",
    "Other"
    ]


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Home page"""
    items = db.execute("SELECT * FROM products")
    return render_template("index.html", categories=categories, items=items)

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == "POST":
        price = request.form.get("price")
        #check for errors
        if not request.form.get("catergory"):
            return apology("Select a Category", 403)
        #insert into database
        db.execute("INSERT INTO products (user_id, name, catergory, description, price, email) VALUES (?,?,?,?,?,?)",
        session["user_id"], request.form.get("product_name"), request.form.get("catergory"), request.form.get("description"), price, request.form.get("email"))

        return redirect("/")
    else:
        return render_template("sell.html", categories=categories)

@app.route("/wishlist", methods=["GET", "POST"])
@login_required
def wishlist():
    if request.method == "POST":
        db.execute("INSERT INTO wishlist (user_id, product_id) VALUES(?,?)", session["user_id"], request.form.get("product_id"))
        return redirect("/wishlist")
    else:
        rows = db.execute("SELECT * FROM products WHERE id IN (SELECT product_id FROM wishlist WHERE user_id = :id)", id = session["user_id"])
        return render_template("wishlist.html", rows=rows)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """register new user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        #check for input errors
        if not username or not password:
            return apology("Please fill up the required fields", 403)
        if password != request.form.get("confirmation"):
            return apology("Passwords do not match!", 403)
        if db.execute("SELECT * FROM users WHERE username = ?", username):
            return apology("THIS USERNAME ALREADY EXISTS!")
        
        #add the user to the database
        db.execute("INSERT INTO users (username,hash) VALUES (?, ?)", username, 
        generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

        #log user in
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/reset", methods=["GET", "POST"])
def reset():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Ensure new passwors was submitted
        if not request.form.get("nw_password"):
            return apology("must provide a new password", 403)

        # update the database for the new password
        db.execute("UPDATE users SET hash = :nwpw WHERE id = :id", nwpw=generate_password_hash(
            request.form.get("nw_password"), method='pbkdf2:sha256', salt_length=8), id=rows[0]["id"])
        return redirect("/login")

    else:
        return render_template("reset.html")

@app.route("/<string:name>", methods=["GET", "POST"])
@login_required
def category(name):
    products = db.execute("SELECT * FROM products WHERE catergory = ?", name)
    return render_template("products.html", items=products, name=name)

@app.route("/myitems", methods=["GET", "POST"])
@login_required
def myitems():
    if request.method == "GET":
        products = db.execute("SELECT * FROM products WHERE user_id = ?", session["user_id"])
        return render_template("myitems.html", items=products)
    else:
        db.execute("DELETE FROM products WHERE id = ?", request.form.get("id"))
        return redirect("/myitems")

@app.route("/remove", methods=["GET", "POST"])
def remove():
    if request.method == "POST":
        db.execute("DELETE FROM wishlist WHERE user_id = ? AND product_id = ?", 
        session["user_id"], request.form.get("id"))
        return redirect("/wishlist")

@app.route("/search")
def search():
    prdcts = db.execute("SELECT * FROM products WHERE name LIKE ?", "%" + request.args.get("q") + "%")
    return render_template("products.html", items=prdcts, name=request.args.get("q"))

@app.route("/contact", methods=["GET", "POST"])
def contact():
    rows = db.execute("SELECT * FROM products WHERE id= ?", request.form.get("id"))
    msg = Message(rows[0]["name"], recipients=[rows[0]["email"]])
    msg.body = request.form.get("message")
    mail.send(msg)
    return redirect("/")