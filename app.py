# set of model
from flask import Flask, render_template, request, redirect, session, abort
from flask_sqlalchemy import SQLAlchemy  # model of database
from datetime import datetime  # for time posts
from flask_admin import Admin  # model for admin department
from flask_admin.contrib.sqla import ModelView

##############################################################

# for flask and database sqlite
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['FLASK_ADMIN_SWATCH'] = 'Simplex'
app.config['SECRET_KEY'] = 'cisco'
db = SQLAlchemy(app)


# classs for posts
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)


# class for register
class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))

    def __repr__(self):
        return f"Register('{self.username}', '{self.email}')"



# class for security admin
class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)


# admin for bootstrap and the classes that view
admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(SecureModelView(Register, db.session))
admin.add_view(SecureModelView(BlogPost, db.session))


##################################################
# department for routes group
# main page
@app.route('/')
def index():
    return render_template('index.html')


# route for posts
# see the posts
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)


# delete the posts only for users
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


# for edit the posts only for users
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


# for add the posts only for users
@app.route('/posts/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts') 
    else:
        return render_template('addpost.html')


#############################################################
# page for ghosts only
@app.route('/posts/ghost', methods=['GET', 'POST'])
def ghost():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts/ghost')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('ghost.html', posts=all_posts)


# for register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = Register(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/posts')


# for register route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('register.htmL')




# for sign route
@app.route("/signin")
def signin():
    return render_template('signin.html')


# the users that register
@app.route('/users')
def users():
    users = Register.query.all()
    return render_template('users.html', users=users)


######################################
# Admin login and logout
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("email") == "jakub.szygula@polsl.pl" and request.form.get(
                "password") == "123456" or request.form.get("email") == "adam.domanski@polsl.pl" and request.form.get(
                "password") == "123456" or request.form.get("email") == "dariusz.marek@polsl.pl" and request.form.get(
                "password") == "123456":
            session['logged_in'] = True
            return render_template("adminpage.html")
        else:
            return render_template("login.html", failed=True)
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/about")
def about():

    return render_template("about.html")

@app.route("/contact")
def contact():

    return render_template("contact.html")

@app.route("/adminpage")
def adminpage():

    return render_template("adminpage.html")
@app.route("/report")
def report():

    return render_template("report.html")

if __name__ == "__main__":
    app.run(debug=True)
