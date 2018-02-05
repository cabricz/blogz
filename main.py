from flask import request, redirect, render_template, session, flash
import cgi
from models import User, Blog
from app import db, app

def isvalid(text):
    if 2 < len(text) < 21:
        return True
    else:
        return False

@app.before_request
def require_login():
    allowed_routes = ["login", "signup", "index", "blog"]
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect("/login")

@app.route("/")
def index():
    user = User.query.all()
    return render_template("index.html", user=user)

@app.route("/blog")
def blog():
    id = request.args.get("id")
    if id:
        user = User.query.all()
        blog = Blog.query.filter_by(id=id).all()
        return render_template("blog.html", blog=blog, user=user)

    user = request.args.get("user")
    if user:
        owner = User.query.filter_by(username=user).first()
        blog = Blog.query.filter_by(owner=owner).all()
        return render_template("blog.html", blog=blog, user=user)
        
    else:
        user = User.query.all()
        blog = Blog.query.all()
        return render_template("blog.html", blog=blog, user=user)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if not user:
            flash("Username does not exist.", "error")
        elif not user.password == password:
            flash("Incorrect password.", "error")
        else:
            session["username"] = username
            flash("Logged in", "bold")
            print(session)
            return redirect("/newpost")

    return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    del session["username"]
    return redirect("/blog")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]

        username_error = ""
        password_error = ""
        verify_error = ""

        existing_user = User.query.filter_by(username=username).first()

        if len(username) == 0:
            username_error = "Please enter username."
        else:
            if existing_user:
                username_error = "Username already exists."
            else:
                if not isvalid(username):
                    username_error = "Username must be between 3 and 20 characters long."
        
        if len(password) == 0:
            password_error = "Please enter password."
        else:
            if not isvalid(password):
                password_error = "Password must be betweeen 3 and 20 characters long."
        
        if len(verify) == 0:
            verify_error = "Plese enter password verification."
        else:
            if not password == verify:
                verify_error = "Passwords must match."

        if not username_error and not password_error and not verify_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session["username"] = username
            flash("Welcome " + username + ". Thanks for signing up!", "bold")
            return redirect("/newpost")
        else:
            return render_template("signup.html", username=username, password=password, verify=verify, username_error=username_error, password_error=password_error, verify_error=verify_error)

    else:
        return render_template("signup.html")

@app.route("/newpost", methods=["POST", "GET"])
def newpost():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        owner = User.query.filter_by(username=session["username"]).first()

        if title and body:
            post = Blog(title, body, owner.id)
            db.session.add(post)
            db.session.commit()
            post_id = str(post.id)
            return redirect("/blog?id={0}".format(post_id))
        else:
            flash("Please enter a title and content for your new blog post.", "error")
            return render_template("newpost.html", title=title, body=body)

    return render_template("newpost.html")

if __name__ == "__main__":
    app.run()