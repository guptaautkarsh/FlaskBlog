from crypt import methods
from datetime import datetime
from fileinput import filename

import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from blog import app, db, bcrypt, mail
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/home")
@login_required
def hello():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=4, page=page)
    return render_template("home.html", post=posts)


@app.route('/register', methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = RegistrationForm() #instance of class
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        flash("Your Account has been created! You can now log in" , 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/", methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = LoginForm()  # instance of class
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Logged In Successfully as {}".format(user.username), 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('hello'))
        else:
            flash("Login Unsuccessful, Check your credentials" , 'danger')
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
@login_required
def logout():
    user = current_user.username
    logout_user()
    flash(f"{user}! You are now logged out ", "success")
    return redirect(url_for('login'))

def save_picture(pic):
    random_hex = secrets.token_hex(8) #just to make file name unique
    f_name, f_ext = os.path.splitext(pic.filename) #.filename to extract filename from the uploaded pic
    picture_fn = random_hex + f_ext
    # now we need to get full path where this image will be stored
    save_picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
    pic.save(save_picture_path) #save pic to that path
    # delete existing photo in static
    if current_user.image_file != 'default.jpg':
        delete_picture_path = os.path.join(app.root_path, 'static/profile_pic', current_user.image_file)
        os.remove(delete_picture_path)

    return picture_fn #returning image name so we can use it to change in database and template


@app.route('/account', methods=['GET', 'POST'])
@login_required     #need to log in before access account route
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for('account')) #else it will rander template and post data again
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pic/{}'.format(current_user.image_file))
    return render_template('account.html', title='Account' ,image_file=image_file, form=form)


@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been posted', 'success')
        return redirect(url_for('hello'))
    return render_template('create_post.html', title='New_Post', form=form)


@app.route('/post/<int:post_id>') #if /post/312 is passed means 312 is the value of post_id variable
def post(post_id):
    user_post = Post.query.get_or_404(post_id) #404 error if not exist
    return render_template('post.html', title=user_post.title, post=user_post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    user_post = Post.query.get_or_404(post_id)
    if user_post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        user_post.title = form.title.data
        user_post.content = form.content.data
        db.session.commit()
        flash('Your post updated successfully', 'success')
        return redirect(url_for('post', post_id=user_post.id))
    elif request.method == 'GET':
        form.title.data = user_post.title
        form.content.data = user_post.content
    return render_template('create_post.html', title="Update Post", form=form)


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    user_post = Post.query.get_or_404(post_id)
    if user_post.author != current_user:
        abort(403)

    db.session.delete(user_post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('hello'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).paginate(per_page=3, page=page)
    return render_template("user_posts.html", posts=posts, user=user)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='utkarshgupta3125@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password , click on the link below:
{url_for('reset_token', token=token, _external=True)}
    
If you didn't make this request, ignore this mail.
'''
    mail.send(msg)

@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent to reset your password", "info")
        return redirect(url_for('login'))
    return render_template('reset_request.html',title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is invalid or token expired. Apply again","warning")
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your Password has been updated! You can now log in", 'success')
        return redirect(url_for('login'))

    return render_template('reset_token.html',title='Reset Password', form=form)