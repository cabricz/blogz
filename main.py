from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://build-a-blog:sifra@localhost:8889/build-a-blog"
app.config["SQLALCHEMY_ECHO"] = True
app.secret_key = "2PJeO9VGXOoJTl"

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

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
            db.session.add(Blog(title, body))
            db.session.commit()
            id = Blog.query.filter_by(title=title,body=body).first()
            return redirect("/blog?id={0}".format(id.id))
        else:
            flash("Please enter a title and content for your new blog post.", "error")
            return render_template("newpost.html", title=title, body=body)

    return render_template("newpost.html")

if __name__ == "__main__":
    app.run()