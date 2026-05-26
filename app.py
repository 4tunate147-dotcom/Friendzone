from flask import Flask, render_template, request, redirect, url_for, flash, session
from model import FriendList, db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os 

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

# App Key
app.config['SECRET_KEY'] = 'secret_key'

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    page = 'proof it that i understand'
    return render_template ("about.html", my_page=page)

@app.route('/friend_list')
def friend_list():
    friend_list = FriendList.query.all()
    return render_template("friend_list.html", friends=friend_list)

@app.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    errors = {}
    
    if request.method == 'POST':
        # 1. Get and strip data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        birthday = request.form.get('birthday', '').strip()
        
        # 2. Validation Logic
        if not name:
            errors['name_err'] = 'Name is required'
        
        if not email:
            errors['email_err'] = 'Email is required'
        elif '@' not in email:
            errors['email_err'] = 'Invalid email address'

        # Check if email already exists in database
        if email:
            existing_friend = FriendList.query.filter_by(email=email).first()
            if existing_friend:
                errors['email_err'] = 'This email is already registered in our system.'
            
        if not birthday:
            errors['birthday_err'] = 'Birthday is required'
            
        # 3. Stop if there are errors
        if errors:
            return render_template('add_friend.html', errors=errors)

        # 4. Process Data & Save
        try:
            dob = datetime.strptime(birthday, "%Y-%m-%d").date()
           
            filename = ''
            # File handling
            if 'upload' in request.files and request.files['upload'].filename != '':
                file = request.files['upload']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Database operation
            new_friend = FriendList(name=name, email=email, dob=dob, profile_pix=filename)
            db.session.add(new_friend)
            db.session.commit()

            flash('Record created successfully', 'success')
            return redirect(url_for('friend_list'))

        except ValueError:
            # This handles invalid date formats
            errors['birthday_err'] = 'Invalid date format'
            return render_template('add_friend.html', errors=errors)
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            return render_template('add_friend.html', errors=errors)

    return render_template('add_friend.html', errors=errors)

# @app.route('/add_friend', methods=['GET', 'POST'])
# def add_friend():
    errors = {}
    
    if request.method == 'POST':
        # 1. Get and strip data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        birthday = request.form.get('birthday', '').strip()

        # user_exist = FriendList.query.filter_by(email=email).first()
        # if user_exist:
        #     flash('User Already Exist', 'Danger')
        
        # 2. Validation Logic
        if not name:
            errors['name_err'] = 'Name is required'
        
        if not email:
            errors['email_err'] = 'Email is required'
        elif '@' not in email:
            errors['email_err'] = 'Invalid email address'
            
        if not birthday:
            errors['birthday_err'] = 'Birthday is required'
            
        # 3. Stop if there are errors
        if errors:
            return render_template('add_friend.html', errors=errors)

        # 4. Process Data & Save
        try:
            dob = datetime.strptime(birthday, "%Y-%m-%d").date()
            filename = ''
            
            # File handling
            if 'upload' in request.files and request.files['upload'].filename != '':
                file = request.files['upload']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Database operation
            new_friend = FriendList(name=name, email=email, dob=dob, profile_pix=filename)
            db.session.add(new_friend)
            db.session.commit()

            flash('Record created successfully', 'success')
            return redirect(url_for('friend_list'))

        except ValueError:
            # This handles invalid date formats
            errors['birthday_err'] = 'Invalid date format'
            return render_template('add_friend.html', errors=errors)
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            return render_template('add_friend.html', errors=errors)

    return render_template('add_friend.html', errors=errors)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_friend(id):

    friend = FriendList.query.get_or_404(id)

    if request.method == 'POST':

        friend.name = request.form.get('name')
        friend.email = request.form.get('email')
        birthday = request.form.get('birthday')
        friend.dob = datetime.strptime(birthday,'%Y-%m-%d').date()
        
        picture = request.files['upload']

        if picture.filename != '':

            picture.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    picture.filename
                )
            )

        friend.profile_pix = picture.filename

        db.session.commit()

            # friend['picture'] = picture.filename

        return redirect(url_for('friend_list'))

    return render_template('edit_friend.html', friend=friend)

@app.route('/delete/<int:id>')
def delete_friend(id):

    friend = FriendList.query.get_or_404(id)

    db.session.delete(friend)
    db.session.commit()

    return redirect(url_for('friend_list'))

if __name__ == "__main__":
    app.run(debug=True)

# @app.route('/add_friend', methods=['GET', 'POST'])
# def add_friend():
#     errors = {}
#     if request.method == 'POST':

#         name = request.form['name']
#         email = request.form['email']
#         birthday = request.form['birthday']
#         dob = datetime.strptime(birthday, "%Y-%m-%d").date()
#         filename = ""

#         user_exist = FriendList.query.filter_by(email=email).first()
#         if user_exist:
#             flash('user already exist', 'danger')
#             return render_template('add_friend.html')


#         if request.files['upload']:
#             files = request.files['upload']
#             filename = secure_filename(files.filename)

#             files.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

#         new_friend = FriendList(name=name, email=email, dob=dob, profile_pix=filename)
#         db.session.add(new_friend)
#         db.session.commit()

#         flash('Record created successfully', 'success')
#         return redirect(url_for('friend_list'))
    
#     return render_template('add_friend.html')


