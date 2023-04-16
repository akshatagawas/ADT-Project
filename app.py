from flask import Flask, render_template, request, json, jsonify, redirect, session, flash, url_for
from flaskext.mysql import MySQL
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import generate_password_hash, check_password_hash




app = Flask(__name__)
app.secret_key = "barneysboard"


# Define a list of protected paths that require authentication
protected_paths = ['/dashboard']

# Define a list of public paths that do not require authentication
public_paths = ['/', '/register']

# Define a function to check if the user is authenticated
def is_authenticated():
    return 'UID' in session

# Define a function to redirect the user to the login page if they are not authenticated
def redirect_unauthenticated():
    return redirect('/')

# Intercept incoming requests and check if the user is authenticated before allowing them to access protected paths
@app.before_request
def authenticate_user():
    if request.path in public_paths:
        return
    elif request.path in protected_paths:
        if not is_authenticated():
            return redirect_unauthenticated()
    else:
        return



# MySQL connection
mysql = MySQL()


# MySQL configurations 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'task_manager'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# App routes
@app.route("/")
def main():
    return render_template('Login.html')

# @app.route("/dashboard")
# def dashboard():
#     return render_template('dashboard.html')


@app.route('/register')
def register():
    return render_template('Register.html')

@app.route('/api/signUp',methods=['POST'])
def signUp():
    # read the posted values from the UI 
    _firstname = request.form['firstname']
    _lastname = request.form['lastname']
    _email = request.form['email']
    _password = request.form['password']

    # Establish connection
    conn = mysql.connect()

    # Define a cursor
    cursor = conn.cursor()

    # Hashed Password
    salt_length = 8
    hash_length = 32
    # _hashed_password = generate_password_hash(_password, method='sha256', salt_length=salt_length)[:hash_length]
    _hashed_password = generate_password_hash(_password)

    # Call procedure createUser
    cursor.callproc('createUser',(_firstname,_lastname,_email,_hashed_password))

    # Check if user is created
    data = cursor.fetchall()


    if len(data) == 0:
        # Commit the transaction and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        # Prepare the success message and the redirect URL
        message = {'success': True, 'message': 'User created successfully!'}

        # Return the success message as a JSON object with the redirect URL and HTTP status code 200
        return redirect("/")
    else:
        # Prepare the error message
        message = {'success': False, 'error': data}

        # Return the error message as a JSON object with HTTP status code 400
        return jsonify(message), 400
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get login information
        print(request.form)
        username = request.form['email']
        password = request.form['password']

        


        # Query the "users" table to verify that the username and password are valid
        # Establish connection
        conn = mysql.connect()

        # Define a cursor
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE EMAIL = %s"
        values = (username,)
        cursor.execute(query, values)
        user = cursor.fetchone()

       

        if user is not None:
            # If the user exists, validate the password
            hashed_password_from_db = user[2]
            res = check_password_hash(hashed_password_from_db,password)
            # message = {'success': True, "hashed_pass":hashed_password_from_db, "pass":password, "Ifsame":res}

            # return message

            if res:
                # If the password is valid, set the user session and redirect the user to the profile page
                session['UID'] = user[0]
                session['username'] = user[1]
                # message = {'success': True, "user":user[1]}
                # return message
                flash(f'Welcome {user[1]}', 'success')
                return redirect('/dashboard')
            else:
                # If the password is not valid, show the login form with an error message
                flash('Incorrect username or password', 'danger')
                return render_template('Login.html')
                # message = {'success': False, "error":"Invalid Password"}
                # return(message)
        else:
            # If the user does not exist, show the login form with an error message
            flash('Incorrect username or password', 'danger')
            return render_template('Login.html')
            # message = {'success': False, "error":"No user found with this email"}
            # return(message)

    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    # Check if user is authenticated
    if not is_authenticated():
        return redirect_unauthenticated()
    
    # Render dashboard page for authenticated users
    return render_template('dashboard.html')



# # Profile page
# @app.route('/profile')
# def profile():
#     if 'user_id' in session:
#         # Get the user's information from the database
#         cursor = db.cursor()
#         query = "SELECT * FROM users WHERE id = %s"
#         values = (session['user_id'],)
#         cursor.execute(query, values)
#         user = cursor.fetchone()

#         if user is not None:
#             # Render the profile page with the user's information
#             return render_template('profile.html', user=user)
#         else:
#             # If the user does not exist, show an error message and redirect to the login page
#             flash('User not found', 'danger')
#             return redirect(url_for('login'))
#     else:
#         # If the user is not logged in, redirect to the login page
#         flash('Please log in', 'warning')
#         return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


        

if __name__ == "__main__":
    app.run()