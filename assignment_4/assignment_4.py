from flask import Blueprint
from settings import DB
from flask import Flask, redirect
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify, json
import requests
import mysql.connector
from app import app

import random

assignment_4 = Blueprint('assignment_4', __name__,
                         static_folder='static',
                         static_url_path='/assignment_4',
                         template_folder='templates')


@assignment_4.route('/assignment4')
def assignment_4_func():
    return render_template('assignment4.html')


# ------------------------------------------------- #
# ------------- DATABASE CONNECTION --------------- #
# ------------------------------------------------- #
def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(**DB)
    #connection = mysql.connector.connect(host='localhost',
     #                                    user='root',
      #                                   passwd='root',
       #                                  database='users')
    cursor = connection.cursor(named_tuple=True)
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

#-------------------------- Part A ---------------------------#

# -----------------------------read list--------------------#
@app.route('/assignment_4')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment4.html', users_list=users_list)


# -------------------- INSERT --------------------- #
@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    id = request.form['id']
    user_name = request.form['user_name']
    email = request.form['email']
    last_name = request.form['last_name']
    age = request.form['age']
    nick_name = request.form['nick_name']
    session['INSERTED'] = True
    session['DELETED'] = False
    session['UPDATE'] = False
    user_exist = "select * FROM users WHERE id='%s';" % id
    users_list = interact_db(user_exist, query_type='fetch')
    if len(users_list) > 0:
        session['insert_message'] = "sorry, we already have this user "
    else:
        query = "INSERT INTO users(id, user_name, email, last_name, age, nick_name) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
        id, user_name, email, last_name, age, nick_name)
        interact_db(query=query, query_type='commit')
        session['insert_message'] = "registration succeeded!"
    return redirect(url_for('users'))


# -------------------- DELETE --------------------- #
@assignment_4.route('/delete_user', methods=['POST'])
def delete_user():
    id = request.form['id']
    session['INSERTED'] = False
    session['UPDATE'] = False
    session['DELETED'] = True

    check_query = 'select * from users'
    before_change_users = interact_db(check_query, query_type='fetch')

    session['delete_message'] = "user deleted"

    query = "DELETE FROM users WHERE id='%s';" % id
    interact_db(query, query_type='commit')

    check_query ='select * from users'
    after_change_users = interact_db(check_query, query_type='fetch')
    if len(before_change_users) > len(after_change_users):
        session['delete_message'] = "delete user succeeded"
    else:
        session['delete_message'] = "sorry, user not exist"
    return redirect(url_for('users'))


# ----------------------------------- UPDATE --------------------------------------#
@assignment_4.route('/update_user', methods=['POST'])
def update_user():
    id = request.form['id']
    user_name = request.form['user_name']
    email = request.form['email']
    last_name = request.form['last_name']
    age = request.form['age']
    nick_name = request.form['nick_name']
    session['INSERTED'] = False
    session['DELETED'] = False
    session['UPDATE'] = True
    session['update_message'] = "update succeeded"
    user_exist = "select * FROM users WHERE id='%s';" % id
    users_list = interact_db(user_exist, query_type='fetch')
    if len(users_list) > 0:
        connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='users')
        updateCursor = connection.cursor()
        updateCursor.execute('''
        UPDATE users
        SET user_name = %s, email = %s, last_name = %s, age = %s, nick_name = %s
        WHERE id = %s
        ''', (user_name, email, last_name, age, nick_name, id))
        connection.commit()
        session['update_message'] = "update succeeded"
    else:
        session['update_message'] = "sorry, user not exist"
    return redirect(url_for('users'))


# -------------------- assignment4_users_PartB --------------------- #
# --------------part B.2+3
@app.route('/assignment4/users')
def assignment4_users_PartB3():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    dict_user_list = []
    for user in users_list:
        user_to_dict = {
            'id': user.id, 'user name': user.user_name, 'last name': user.last_name,
            'age': user.age, 'nick name': user.nick_name, 'email': user.email
        }
        dict_user_list.append(user_to_dict)
    return jsonify(dict_user_list)


# @assignment_4.route('/assignment4/users1')
# def assignment4_users_PartB1():
#   query = 'select * from users'
#  users_list = interact_db(query, query_type='fetch')
# users_json = json.dumps(users_list)
# return render_template('assignment4_partB_3.html', users_json=users_json)


# -------------------- assignment4_outer_source_PartB ------------------------ #
# -------------------- fronted ------------------------ #
@app.route('/assignment4/outer_source')
def fetch_front_func():
    session.clear()
    return render_template('fetch_back_front.html')


# ------------------------------------beckend---------------------------------#

@assignment_4.route('/fetch_be')
def fetch_beck_func():
    if 'num_id' in request.args:
        id = int(request.args['num_id'])
        session['num'] = id
        picked_user = get_users(id)
        save_users_to_session(picked_user)
    else:
        session.clear()
    return render_template('fetch_back_front.html')


def get_users(id):
    picked_user = []
    res = requests.get(f'https://reqres.in/api/users/{id}')
    picked_user.append(res.json())
    return picked_user


def save_users_to_session(picked_user):
    users_list_to_save = []
    for user in picked_user:
        picked_user_dict = {
            'data': {
                'avatar': user['data']['avatar']
            },
            'email': user['data']['email'],
            'first_name': user['data']['first_name'],
        }
        users_list_to_save.append(picked_user_dict)
    session['picked_user'] = users_list_to_save

# ------------------------------------Part C---------------------------------#

@assignment_4.route('/assignment4/restapi_users', defaults={'USER_ID': 1})
@assignment_4.route('/assignment4/restapi_users/<int:USER_ID>')
def assignment4_restapi_users(USER_ID):
    query_users = "select * FROM users WHERE id='%s';" % USER_ID
    restapi_user = interact_db(query_users, query_type='fetch')

    if len(restapi_user) > 0:
        user = json.dumps(restapi_user)
        session['errorMessage'] = ''
        return render_template('Part_C.html', user=user)
    else:
        error_Message = 'User not exist'
        session['errorMessage'] = json.dumps(error_Message)
        return render_template('Part_C.html')
