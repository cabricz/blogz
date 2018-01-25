from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://blogz:blogz@localhost:8889/blogz"
app.config["SQLALCHEMY_ECHO"] = True
app.secret_key = "2PJeO9VGXOoJTl"

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner_id = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    blogs = db.relationship("Blog", backref="owner")

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route("/")
def index():
    return redirect("/blog")

@app.route("/blog")
def blog():
    id = request.args.get("id")
    if id:
        blog = Blog.query.filter_by(id=id).all()
        return render_template("blog.html", blog=blog)
    else:
        blog = Blog.query.all()
        return render_template("blog.html", blog=blog)

@app.route("/newpost", methods=["POST", "GET"])
def newpost():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        if title and body:
            post = Blog(title,body)
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