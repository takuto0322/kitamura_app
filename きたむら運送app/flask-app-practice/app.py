from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import session,redirect,url_for
from hashlib import sha256
from app import key

app = Flask(__name__)
app.secret_key = key.SECRET_KEY


@app.route("/")
@app.route("/index")
def index():
    if "user_name" in session:
        name = session["user_name"]
        all_onegai = OnegaiContent.query.all()
        return render_template("index.html",name=name,all_onegai=all_onegai)
    else:
        return redirect(url_for("top",status="logout"))


@app.route("/add",methods=["post"])
def add():
    title = request.form["title"]
    body = request.form["body"]
    content = OnegaiContent(title,body,datetime.now())
    db_session.add(content)
    db_session.commit()
    return redirect(url_for("index"))


@app.route("/update",methods=["post"])
def update():
    content = OnegaiContent.query.filter_by(id=request.form["update"]).first()
    content.title = request.form["title"]
    content.body = request.form["body"]
    db_session.commit()
    return redirect(url_for("index"))


@app.route("/delete",methods=["post"])
def delete():
    id_list = request.form.getlist("delete")
    for id in id_list:
        content = OnegaiContent.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return redirect(url_for("index"))


@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html",status=status)


@app.route("/login",methods=["post"])
def login():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        if user.hashed_password == hashed_password:
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top",status="wrong_password"))
    else:
        return redirect(url_for("top",status="user_notfound"))


@app.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("newcomer.html",status=status)


@app.route("/registar",methods=["post"])
def registar():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        return redirect(url_for("newcomer",status="exist_user"))
    else:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(user_name, hashed_password)
        db_session.add(user)
        db_session.commit()
        session["user_name"] = user_name
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top",status="logout"))


if __name__ == "__main__":
    app.run(debug=True)


# app = Flask(__name__)
# app.secret_key = key.SECRET_KEY

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)
# db.create_all()

# class Post(db.Model):

#     __tablename__ = "posts"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     date = db.Column(db.Text())
#     title = db.Column(db.Text())
#     content = db.Column(db.Text())
#     commit = db.Column(db.Integer)


# @app.route("/registar",methods=["post"])
# def registar():
#     user_name = request.form["user_name"]
#     user = User.query.filter_by(user_name=user_name).first()
#     if user:
#         return redirect(url_for("newcomer",status="exist_user"))
#     else:
#         password = request.form["password"]
#         hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
#         user = User(user_name, hashed_password)
#         db_session.add(user)
#         db_session.commit()
#         session["user_name"] = user_name
#         return redirect(url_for("index"))

# # @app.route('/') # ルート(/)ページURLにリクエストが送られた時の処理
# # def index():

# #     posts = Post.query.all()
# #     return render_template("index.html", posts = posts)

# @app.route("/")
# @app.route("/index")
# def index():
#     if "user_name" in session:
#         name = session["user_name"]
#         all_onegai = OnegaiContent.query.all()
#         return render_template("index.html",name=name,all_onegai=all_onegai)
#     else:
#         return redirect(url_for("top",status="logout"))

# @app.route('/show/<int:id>')
# def show(id):
#     post = Post.query.get(id)
#     return render_template("show.html", post = post)

# @app.route('/new')
# def new_post():

#     return render_template("new.html")

# @app.route('/create', methods=["POST"])
# def create_post():

#     new_post = Post()
#     new_post.title = request.form["title"]
#     new_post.content = request.form["content"]
#     new_post.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
#     new_post.commit = 0
#     db.session.add(new_post)
#     db.session.commit()

#     return redirect(url_for('.index'))

# @app.route('/edit/<int:id>')
# def edit_post(id):

#     post = Post.query.get(id)

#     return render_template("edit.html", post = post)

# @app.route('/update/<int:id>', methods=["POST"])
# def update_post(id):

#     post = Post.query.get(id)
#     post.title = request.form["title"]
#     post.content = request.form["content"]
#     post.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
#     db.session.commit()

#     return redirect(url_for('.index'))

# @app.route('/done/<int:id>')
# def done_post(id):

#     post = Post.query.get(id)
#     post.commit = 1
#     post.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
#     db.session.commit()
#     posts = Post.query.all()

#     return redirect(url_for('.index'))

# @app.route('/undone/<int:id>')
# def undone_post(id):

#     post = Post.query.get(id)
#     post.commit = 0
#     post.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
#     db.session.commit()
#     posts = Post.query.all()

#     return redirect(url_for('.index'))

# @app.route('/destroy/<int:id>')
# def destroy(id):

#     post = Post.query.get(id)
#     db.session.delete(post)
#     db.session.commit()
#     posts = Post.query.all()

#     return redirect(url_for('.index'))

# @app.route('/destroy/alldone')  
# def destroy_alldone():

#     posts_done = Post.query.filter_by(commit=1).all()
#     for i in posts_done:
#         db.session.delete(i)
#     db.session.commit()
#     posts = Post.query.all()

#     return redirect(url_for('.index'))


# @app.route("/top")
# def top():
#     status = request.args.get("status")
#     return render_template("top.html",status=status)

# @app.route("/login",methods=["post"])
# def login():
#     user_name = request.form["user_name"]
#     user = User.query.filter_by(user_name=user_name).first()
#     if user:
#         password = request.form["password"]
#         hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
#         if user.hashed_password == hashed_password:
#             session["user_name"] = user_name
#             return redirect(url_for("index"))
#         else:
#             return redirect(url_for("top",status="wrong_password"))
#     else:
#         return redirect(url_for("top",status="user_notfound"))


# @app.route("/newcomer")
# def newcomer():
#     status = request.args.get("status")
#     return render_template("newcomer.html",status=status)


# @app.route("/logout")
# def logout():
#     session.pop("user_name", None)
#     return redirect(url_for("top",status="logout"))

# if __name__ == "__main__":
#     app.run(debug=True)