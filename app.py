from db_config import *

#function to get all the mail id




@app.route('/',methods =['GET','POST'])
def login():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password = hashlib.md5(password.encode())
        password = password.hexdigest()
        cursor.execute('select * from user_data where mail_id =%s and password = %s',(email,password))
        account  = cursor.fetchone()
        if account:
              session['email'] = email
              return jsonify({'status':'success'})

        else:
             return jsonify({'status':'failure'})
    elif (not session.get("email") is None):
        return redirect(url_for('inbox'))
    else:
        #getting the mailid'
        cursor.execute('select mail_id from user_data')
        mail_ids = cursor.fetchall()
        mail_ids = [x[0] for x in mail_ids]
        return render_template('login_sign_up.html',mail_ids=mail_ids)


@app.route('/register',methods =['GET','POST'])
def register():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        flag = 0
        username = request.form['username']
        mail = request.form['mail']
        password = request.form['password']
        password = hashlib.md5(password.encode())
        password = password.hexdigest()
        mobile = request.form['mobile']

        query = "INSERT INTO user_data (mail_id,name,password,phone_no) VALUES (%s,%s,%s,%s)"
        values = (mail,username,password,mobile)
        cursor.execute(query, values)
        try:
            mysql.connection.commit()
            flag = 1
        except:
            flag= 0
            print('failed to commit')
            mysql.connection.rollback()
        if flag:
            email =[]
            email.append(mail)
            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            if(insert_receiver("admin@dummymail.com","Dummymail", email,"Welcome", "Thanks for registering in dummymail ", date_time)):

                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'failure'})
        else:
             return jsonify({'status':'failure'})


#inbox logic
@app.route('/inbox',methods=['GET','POST'])
def inbox():
    if 'email' in session:
        cursor = mysql.connection.cursor()
        email = session.get('email')
        cursor.execute('select * from user_data where mail_id =%s', (email,))
        account = cursor.fetchone()
        account = [x for x in account]




        query = 'select * from receive_mail where receiver_mail =%s order by id DESC'
        values = (email,)
        cursor.execute(query,values)
        inbox = cursor.fetchall()
        inbox = [list(x) for x in inbox]

        #mailid check
        cursor.execute('select mail_id from user_data')
        mail_ids = cursor.fetchall()
        mail_ids = [x[0] for x in mail_ids]
        title = "Inbox"
        return render_template('inbox.html',account=account,inbox=inbox,mail_ids=mail_ids,title=title,count = count_(email))
    else:
        return redirect(url_for('login'))


#sent mail section logic
@app.route('/sent',methods=['GET','POST'])
def sent():
    if 'email' in session:
        cursor = mysql.connection.cursor()
        email = session.get('email')
        cursor.execute('select * from user_data where mail_id =%s', (email,))
        account = cursor.fetchone()
        account = [x for x in account]




        query = 'select * from sent_mail where sender_mail =%s order by id DESC'
        values = (email,)
        cursor.execute(query,values)
        inbox = cursor.fetchall()
        inbox = [list(x) for x in inbox]

        #mailid check
        cursor.execute('select mail_id from user_data')
        mail_ids = cursor.fetchall()
        mail_ids = [x[0] for x in mail_ids]
        title = "Sent Mail"
        return render_template('sent.html',account=account,inbox=inbox,mail_ids=mail_ids,title=title,count = count_(email))
    else:
        return redirect(url_for('login'))


#star messages logic
@app.route('/star',methods=['GET','POST'])
def star():
    if 'email' in session:
        cursor = mysql.connection.cursor()
        email = session.get('email')
        cursor.execute('select * from user_data where mail_id =%s', (email,))
        account = cursor.fetchone()
        account = [x for x in account]

        query = 'select * from receive_mail where receiver_mail =%s and starred = %s order by id DESC'
        values = (email,'1')
        cursor.execute(query, values)
        inbox = cursor.fetchall()
        inbox = [list(x) for x in inbox]

        # mailid check
        cursor.execute('select mail_id from user_data')
        mail_ids = cursor.fetchall()
        mail_ids = [x[0] for x in mail_ids]
        title = "Star"
        return render_template('inbox.html', account=account, inbox=inbox, mail_ids=mail_ids, title=title,count = count_(email))
    else:
        return redirect(url_for('login'))


#view messages inbox logic
@app.route('/view_message_inbox/<string:id>',methods=['GET'])
def view_message_inbox(id):
    if 'email' in session:
        cursor = mysql.connection.cursor()

        email = session.get('email')
        cursor.execute('select * from user_data where mail_id =%s', (email,))
        account = cursor.fetchone()
        account = [x for x in account]

        cursor.execute('select * from receive_mail where id = %s',(id,))
        message = cursor.fetchone()
        message = [x for x in message]

        #read-unread check
        cursor.execute('select read_status from receive_mail where id = %s',(id,))
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.execute('update receive_mail set read_status = %s where id = %s',('1',id))
            mysql.connection.commit()

        # mailid check
        cursor.execute('select mail_id from user_data')
        mail_ids = cursor.fetchall()
        mail_ids = [x[0] for x in mail_ids]
        title = "Message"
        return render_template('view_message_inbox.html',message=message,mail_ids=mail_ids,account=account,title = title,count = count_(email))


#view messages inbox logic
@app.route('/view_message_sent/<string:id>',methods=['GET'])
def view_message_sent(id):
    if 'email' in session:
        cursor = mysql.connection.cursor()

        email = session.get('email')
        cursor.execute('select * from user_data where mail_id =%s', (email,))
        account = cursor.fetchone()
        account = [x for x in account]

        cursor.execute('select * from sent_mail where id = %s',(id,))
        message = cursor.fetchone()
        message = [x for x in message]

        # mailid check
        cursor.execute('select mail_id from user_data')
        mail_ids = cursor.fetchall()
        mail_ids = [x[0] for x in mail_ids]
        title = "Message"
        return render_template('view_message_sent.html',message=message,mail_ids=mail_ids,account=account,title = title,count = count_(email))

#logic to send the mail
@app.route('/send_mail',methods=['GET','POST'])
def send_mail():
    cursor = mysql.connection.cursor()
    sender_email = session.get('email')
    email=request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")

    #get the mail id
    email = list(map(str,email.split(',')))

    #receiver table
    cursor.execute('select name from user_data where mail_id = %s',(sender_email,))
    sender_name = cursor.fetchone()
    sender_name = sender_name[0]
    print(sender_name)

    #insert_receiver
    if(insert_receiver(sender_email,sender_name,email,subject,message,date_time) and insert_sender(sender_email,email,subject,message,date_time)):
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failure'})


#onclick actions with ajax
@app.route('/do_star/<string:id>',methods=['POST','GET'])
def do_star(id):
    cursor = mysql.connection.cursor()
    cursor.execute('update receive_mail set starred = %s where id = %s',(1,id))
    mysql.connection.commit()
    return redirect(url_for('inbox'))

@app.route('/undo_star/<string:id>',methods=['POST','GET'])
def undo_star(id):
    cursor = mysql.connection.cursor()
    cursor.execute('update receive_mail set starred = %s where id = %s',(0,id))
    mysql.connection.commit()
    return redirect(url_for('inbox'))

@app.route('/delete_inbox/<string:id>',methods=['POST','GET'])
def delete_inbox(id):
    cursor = mysql.connection.cursor()
    cursor.execute('delete from receive_mail where id =%s',(id,))
    mysql.connection.commit()
    return redirect(url_for('inbox'))

@app.route('/delete_sent/<string:id>',methods=['POST','GET'])
def delete_sent(id):
    cursor = mysql.connection.cursor()
    cursor.execute('delete from sent_mail where id =%s', (id,))
    mysql.connection.commit()
    return redirect(url_for('sent'))


#logout function
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
