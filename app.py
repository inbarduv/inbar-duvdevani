from flask import Flask, redirect
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector
import requests

app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=40)

@app.route('/')
def homePage_func():  # put application's code here
    session['INSERTED'] = False
    session['DELETED'] = False
    session['UPDATE'] = False
    return render_template('homePage.html')

@app.route('/google')
def google_func():  # put application's code here
    return redirect("https://www.google.com/")


@app.route('/leave_details')
def leave_details_func():  # put application's code here
    session['UPDATE'] = False
    session['INSERTED'] = False
    session['DELETED'] = False
    return render_template('leave_details.html')

@app.route('/assignment3_1')
def about_page():
    session['UPDATE'] = False
    session['INSERTED'] = False
    session['DELETED'] = False
    user_info = {'first name': ' Inbar', 'last_name': ' Duvdevani', 'age': ' 27' , 'home town': ' Hayogev'}
    sports = ['Running', 'Frisbee', 'Basketball']
    movies = ['kill bill', 'pirates of the caribbean', 'space jam', 'treasure planet']
   # session['CHECK'] = 'about'
    return render_template('assignment3_1.html',
                           user_info=user_info,
                           sports=sports,
                           movies=movies)


user_dict = {
    'Inbar': ['Inbar@gmail.com', 'Duvdevani', '27', 'Inbi'],
    'Reut': ['Reut@gmail.com', 'Hochwald', '26', 'Widad'],
    'Rinat': ['Rinat@gmail.com', 'Rozenblum', '25', 'Rino'],
    'Hadar': ['Hadar@gmail.com', 'Malki', '25', 'Hadari'],
    'Shahar': ['Shahar@gmail.com', 'Dumani', '25', 'Shuchi'],
    'Tal': ['Tal@gmail.com', 'Kashi', '27', 'Taltul'],
    'Yael': ['Yael@gmail.com', 'Kachanski', '25', 'Yaeli']
}


@app.route('/assignment3_2', methods=['GET', 'POST'])
def go_to_assignment3_2():
    session['INSERTED'] = False
    session['DELETED'] = False
    session['UPDATE'] = False
    # Get Case
    if request.method == 'GET':
        if 'user_name' in request.args:
            user_name = request.args['user_name']
            if user_name in user_dict:
                return render_template('assignment3_2.html',
                                       user_username=user_name,
                                       user_lastname=user_dict[user_name][1],
                                       user_email=user_dict[user_name][0],
                                       user_age=user_dict[user_name][2],
                                       nickname=user_dict[user_name][3])
            if len(user_name) == 0:
                return render_template('assignment3_2.html',
                                       user_dict=user_dict)
            else:
                return render_template('assignment3_2.html', message='User is not found in the system!')
    # Post Case
    if request.method == 'POST':
        reg_username = request.form['username']
        reg_lastname = request.form['user_lastname']
        reg_email = request.form['email']
        reg_age = request.form['age']
        reg_nickname = request.form['nickname']
        session['username'] = reg_username
        session['user_lastname'] = reg_lastname
        session['email'] = reg_email
        session['age'] = reg_age
        session['nickname'] = reg_nickname
        session['Registered'] = True
        if reg_username in user_dict:
            return render_template('assignment3_2.html', message2='user is already exist!!')
        else:
            new_user = {reg_username: [reg_email, reg_lastname, reg_age, reg_nickname]}
            user_dict.update(new_user)
            return render_template('assignment3_2.html', message2='registration succeeded')

        return render_template('assignment3_2.html')

    return render_template('assignment3_2.html')


@app.route('/session')
def session_func():
    # print(session['CHECK'])
    return jsonify(dict(session))

@app.route('/log_out')
def logout():
    session['Registered'] = False
    session.clear()
    return redirect(url_for('go_to_assignment3_2'))



##-----------------------------------------------assignment_4------------------------------------#

## assignment_4
from assignment_4.assignment_4 import assignment_4
app.register_blueprint(assignment_4)

# ------------------------------------------------- #
# ------------- DATABASE CONNECTION --------------- #
# ------------------------------------------------- #
def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='users')
    cursor = connection.cursor(named_tuple=True) # indicator
    cursor.execute(query)
    #

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

# query = "INSERT INTO try_table_1(name) VALUES ('try_name_1')"
# interact_db(query=query, query_type='commit')
#
# query = "select * from try_table_1"
# query_result = interact_db(query=query, query_type='fetch')
# print(query_result)
# ------------------------------------------------- #
# ------------------------------------------------- #







# @app.route('/insert_user', methods=['GET', 'POST'])
# def insert_user():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         # recheck
#         query = "INSERT INTO users(name, email, password) VALUES ('%s', '%s', '%s')" % (name, email, password)
#         interact_db(query=query, query_type='commit')
#         return redirect('/users')
#     return render_template('insert_user.html', req_method=request.method)


# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# -------------------- DELETE --------------------- #
# ------------------------------------------------- #
@app.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_id = request.form['user_id']
    query = "DELETE FROM users WHERE id='%s';" % user_id
    # print(query)
 #   interact_db(query, query_type='commit')
    return redirect('/users')


# @app.route('/delete_user', methods=['POST'])
# def delete_user():
#     user_id = request.form['id']
#     query = "DELETE FROM users WHERE id='%s';" % user_id
#     interact_db(query, query_type='commit')
#     return redirect('/users')


# ------------------------------------------------- #
# ------------------------------------------------- #

if __name__ == '__main__':
    app.run(debug=True)
