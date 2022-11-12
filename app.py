from flask import Flask, flash, redirect, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension
from forms import FeedbackForm, LoginForm, RegistrationForm
from models import Feedback, User, connect_db, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "SECRET!"

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def homepage():
    if "user_id" in session:
        return redirect('/secret')
    else:
        return redirect("/register")


@app.route('/secret')
def secret():
    if "user_id" in session:
        userId = session['user_id']
        user = User.query.get(userId)
        feedback = Feedback.query.all()
        return render_template('/secret.html', user=user, feedback=feedback)
    else:
        flash("You must be registered and login first!")
        return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.register_user(form)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect('/secret')
    else:
        render_template('/index.html')
        return render_template('/register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form)
        if user:
            flash(f"Welcome back, {user.username}")
            session['user_id'] = user.id
            return redirect('/secret')
        else:
            form.username.errors = ['Invalid username/password.']
            return render_template('/login.html', form=form)
    else:
        return render_template('/login.html', form=form)


@app.route('/edit-user', methods=["GET", "POST"])
def edit():
    userId = session['user_id']
    if "user_id" in session:
        user = User.query.get(userId)
        form = RegistrationForm(obj=user)
        if form.validate_on_submit():
            User.edit_user(form, userId)
            return redirect('/')
        else:
            return render_template('/edit-user.html', form=form, userId=userId)
    else:
        flash(f"Must be registered and login first!")
        return redirect('/')


@app.route('/user/<int:id>/delete', methods=["POST"])
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == session['user_id']:
        db.session.delete(user)
        db.session.commit()
        session.pop("user_id")
        flash("User has been unregistered")
        return redirect('/')
    else:
        flash("You do not have permission to unregister user!")
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop("user_id")
    flash("Goodbye!")
    return redirect('/')


@app.route('/feedback/<int:id>/delete', methods=["POST"])
def delete_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    if feedback.user_id == session['user_id']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback post deleted")
        return redirect('/secret')
    else:
        flash("You do not have permission to delete this post")
        return redirect('/')


@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    if "user_id" in session:
        userId = session['user_id']
        form = FeedbackForm()
        if form.validate_on_submit():
            message = Feedback.save_feedback(userId, form)
            db.session.add(message)
            db.session.commit()
            return redirect('/secret')
        else:
            return render_template('/feedback.html', form=form)
    else:
        flash("Must be registered and login first")
        return redirect('/')
