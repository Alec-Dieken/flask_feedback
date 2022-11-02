from flask import render_template, jsonify, request, redirect, url_for, session, flash
from flask_feedback import app, db
from flask_feedback.forms import RegistrationForm, LoginForm, FeedbackForm
from flask_feedback.models import Users, Feedback, login_required

# ####################################################################################
@app.route('/')
def home():
    if "user_id" in session:
        return redirect(f'users/{session.get("user_id")}')

    return redirect(url_for('register'))

# ####################################################################################
@app.route('/register', methods=['GET', 'POST'])
def register():
    if "user_id" in session:
        return redirect(url_for('secret'))

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = Users.register(username=username, password=password, email=email,
                    first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    else:
        return render_template('register.html', form=form)

# ####################################################################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user_id" in session:
        return redirect(url_for('secret'))

    form = LoginForm()

    if form.validate_on_submit():
        user = Users.authenticate(form.username.data, form.password.data)

        if user:
            session['user_id'] = user.username
            flash('Login successful!')
            return redirect(f'/users/{user.username}')
        else:
            flash('Username and/or password incorrect.')
            return redirect(url_for('login'))

    else:
        return render_template('login.html', form=form)

# ####################################################################################
@app.route('/logout')
def logout():
    if "user_id" in session:
        session.pop('user_id')

    return redirect(url_for('login'))

# ####################################################################################
@app.route('/users/<username>')
@login_required
def homepage(username):
    if username != session.get('user_id'):
        return redirect(f'/users/{session.get("user_id")}')

    user = Users.query.get_or_404(username)
    feedback = user.feedback

    return render_template('homepage.html', user=user, feedback=feedback)

# ####################################################################################
@app.route('/users/<username>/delete', methods=['POST'])
@login_required
def delete_user(username):
    if username != session.get('user_id'):
        return redirect(f'/users/{session.get("user_id")}')

    user = Users.query.get(username)
    feedback = Feedback.query.filter_by(username=username).first()
    if feedback:
        db.session.delete(feedback)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('logout'))

# ####################################################################################
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
@login_required
def add_feedback(username):
    if username != session.get('user_id'):
        return redirect(f'/users/{session.get("user_id")}')

    form = FeedbackForm()

    if form.validate_on_submit():
        feedback = Feedback(title=form.title.data, content=form.content.data, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return render_template('add_feedback.html', form=form)
    
    

# ####################################################################################
@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
@login_required
def edit_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if not feedback or feedback.username != session.get('user_id'):
        return redirect(f'/users/{session.get("user_id")}')

    form = FeedbackForm()
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{session.get("user_id")}')
    else:
        form.title.default = feedback.title
        form.content.default = feedback.content
        form.process()
        return render_template('edit_feedback.html', form=form, feedback=feedback)

# ####################################################################################
@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
@login_required
def delete_feedback(feedback_id):
    
    feedback = Feedback.query.get(feedback_id)

    if not feedback or feedback.username != session.get('user_id'):
        return redirect(f'/users/{session.get("user_id")}')

    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{session.get("user_id")}')


