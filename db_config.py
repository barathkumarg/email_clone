from flask import Flask, request,redirect,url_for, jsonify, render_template,session
from test import *
import hashlib
from flask_mysqldb import MySQL
from datetime import datetime
app = Flask(__name__)
#db configuation
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'YJhCmVseWc'
app.config['MYSQL_PASSWORD'] = 'qowlYr4pay'
app.config['MYSQL_DB'] = 'YJhCmVseWc'

mysql = MySQL(app)


def insert_receiver(sender_email,sender_name,email,subject,message,date_time):
    cursor = mysql.connection.cursor()
    for i in email:
        query = "insert into receive_mail (sender_mail,sender_name,receiver_mail,subject,message,date_time) values(%s,%s,%s,%s,%s,%s)"
        values=(sender_email,sender_name,i,subject,message,date_time)
        cursor.execute(query,values)
        try:

            mysql.connection.commit()
        except:
            print('failed to commit')
            mysql.connection.rollback()
            return False
    return True

def insert_sender(sender_email,email,subject,message,date_time):
    cursor = mysql.connection.cursor()
    for i in email:
        cursor.execute('select name from user_data where mail_id = %s', (i,))
        receiver_name = cursor.fetchone()
        receiver_name = receiver_name[0]

        query = "insert into sent_mail (sender_mail,receiver_name,receiver_mail,subject,message,date_time) values(%s,%s,%s,%s,%s,%s)"
        values=(sender_email,receiver_name,i,subject,message,date_time)
        cursor.execute(query,values)
        try:
            mysql.connection.commit()
        except:
            print('failed to commit')
            mysql.connection.rollback()
            return False
    return True
def count_(email):
    cursor = mysql.connection.cursor()
    print(email)
    cursor.execute('select count(*) from receive_mail where receiver_mail =%s and read_status = %s',(email,'0'))
    count = cursor.fetchone()
    print(count[0])
    return count[0]
