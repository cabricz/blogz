from flask import request, redirect, render_template, session, flash
import cgi
from models import User, Blog
from app import db, app

@app.route("/")
def index():
    return redirect("/blog")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]

        #validate user input

        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = username

        return redirect("/newpost")
    
    else:
        return render_template("signup.html")



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