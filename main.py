from flask import Flask, render_template, request, json, jsonify, redirect, session, flash, url_for
from flask_bcrypt import generate_password_hash, check_password_hash
import pymysql
import ssl
from datetime import datetime
from flask_session import Session


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/task_manager'



app.secret_key = "barneysboard"

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp'
app.config['SESSION_COOKIE_NAME'] = 'my_cookie'
app.config['SECRET_KEY'] = 'secret_key'

Session(app)

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
# mysql = MySQL()


# MySQL configurations 
# app.config['MYSQL_DATABASE_USER'] = 'barney'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'board@123'
# app.config['MYSQL_DATABASE_DB'] = 'task_manager'
# app.config['MYSQL_DATABASE_HOST'] = 'barneysboard.mysql.database.azure.com'
# mysql = MySQL(app)





# SSL/TLS options
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# Connect to MySQL server with SSL/TLS encryption


# App routes
@app.route("/")
def main():
    return render_template('Login.html')


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
    conn = pymysql.connect(
    host='barneysboard.mysql.database.azure.com',
    user='barney',
    password='board@123',
    database='task_manager',
    ssl=ssl_ctx,
    )

    # Define a cursor
    cursor = conn.cursor()

    # Hashed Password
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
        # print(request.form)
        username = request.form['email']
        password = request.form['password']

        


        # Query the "users" table to verify that the username and password are valid
        # Establish connection
        conn = pymysql.connect(
        host='barneysboard.mysql.database.azure.com',
        user='barney',
        password='board@123',
        database='task_manager',
        ssl=ssl_ctx,
        
        )

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

@app.route('/get_data')
def get_data():
    # Fetch data from database and convert it to JSON
    uid = session.get('UID')
   
    # Render dashboard page for authenticated users
    conn = pymysql.connect(
    host='barneysboard.mysql.database.azure.com',
    user='barney',
    password='board@123',
    database='task_manager',
    ssl=ssl_ctx,
    )
    c = conn.cursor()
    c.execute("SELECT * FROM task WHERE UID=%s", (uid,))
    
    rows = c.fetchall()
    
    # Convert timedelta object to string
    data = []
    for row in rows:
        # duration_str = str(row[5])
        data.append({
            'TID': row[0],
            'UID': row[1],
            'TASK_NAME': row[2],
            'TASK_DESCRIPTION': row[3],
            'TASK_STATUS': row[4]

        })

    
    if len(data) != 0:
    
        return jsonify(data)

    else:
        # Prepare the error message
        message = {'success': False, 'error': data}
        return(message)
    


@app.route('/dashboard')
def dashboard():
    
    
    # return render_template('dashboard.html', data=data)
    now = datetime.utcnow()
    return render_template('dashboard.html', now=now)



@app.route('/get_task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        conn = pymysql.connect(
        host='barneysboard.mysql.database.azure.com',
        user='barney',
        password='board@123',
        database='task_manager',
        ssl=ssl_ctx,
        )
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM TASK WHERE TID = %s', (task_id,))
        task = cursor.fetchone()
        if not task:
            return jsonify({'error': f'Task with id {task_id} not found'})
        task_dict = {
            'TID': task[0],
            'UID': task[1],
            'TASK_NAME': task[2],
            'TASK_DESCRIPTION': task[3],
            'TASK_STATUS': task[4]
        }
        return jsonify(task_dict)
    except Exception as e:
        print(f'Error fetching task data: {str(e)}')
        return jsonify({'error': 'Error fetching task data'})
    finally:
        cursor.close()
        conn.close()



# Adding new task to database
@app.route('/new_task', methods=['GET', 'POST'])
def new_task():
    # read the posted values from the UI 
    uid = session.get('UID')
    task_name = request.form['task-name']
    task_description = request.form['task-description']
    task_status = request.form['task-status']



    # Establish connection
    conn = pymysql.connect(
    host='barneysboard.mysql.database.azure.com',
    user='barney',
    password='board@123',
    database='task_manager',
    ssl=ssl_ctx,
    )

    # Define a cursor & insert data
    cursor = conn.cursor()
    cursor.execute('INSERT INTO TASK (UID, TASK_NAME, TASK_DESCRIPTION, TASK_STATUS) VALUES (%s, %s, %s, %s)',
                   (uid, task_name, task_description, task_status))
    conn.commit()
    cursor.close()


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
        return redirect("/dashboard")
    else:
        # Prepare the error message
        message = {'success': False, 'error': data}

        # Return the error message as a JSON object with HTTP status code 400
        return jsonify(message), 400


@app.route('/delete_task/<int:tid>', methods=['DELETE'])
def delete_task(tid):
  conn = pymysql.connect(
    host='barneysboard.mysql.database.azure.com',
    user='barney',
    password='board@123',
    database='task_manager',
    ssl=ssl_ctx,
    )
  cursor = conn.cursor()
  cursor.execute('DELETE FROM TASK WHERE TID = %s', (tid,))
  conn.commit()
  return '', 204


@app.route('/edit_task', methods=['POST'])
def edit_task():
    # Get form data from request
    # data = request.get_json()
    # return(json.dumps(data))
    task_name = request.form['task-name']
    task_id = request.form['task-id']
    task_description = request.form['task-description']
    task_status = request.form['task-status']

    # task_data = {
    #     'task_name': task_name,
    #     'task_id': task_id,
    #     'task_description': task_description,
    #     'task_status': task_status
    # }
    
    # # return the task data as JSON
    # return jsonify(task_data)
    # task_id = data.get('')
    # task_name = data.get('task_name')
    # task_description = data.get('task_description')
    # task_status = data.get('task_status')

    # tid = '13'
    # task_name = 'Task 13'
    # task_description = 'completed'
    # task_status = 'COMPLETE'

    # Connect to database and update task record
    conn = pymysql.connect(
    host='barneysboard.mysql.database.azure.com',
    user='barney',
    password='board@123',
    database='task_manager',
    ssl=ssl_ctx,
    )
    cursor = conn.cursor()
    cursor.execute('UPDATE TASK SET TASK_NAME=%s, TASK_DESCRIPTION=%s, TASK_STATUS=%s WHERE TID=%s',
    (task_name, task_description, task_status, task_id))
    conn.commit()

    # Return success message
    return redirect('/dashboard')


# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


        

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)