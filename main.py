import random
import re
from datetime import datetime
from urllib import request
import ar_master
from flask import Flask, render_template, request, session
import datetime
from test import split_and_store

app = Flask(__name__, static_folder='static',template_folder='templates',static_url_path='/static')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
mm = ar_master.master_flask_code('python_blockchain_banking_refund')
@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/admin_login", methods = ['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['pass'] == 'admin':
            return render_template('admin_home.html',error=error)
        else:
            return render_template('admin.html', error=error)

@app.route("/user")
def user():
    return render_template('user.html')

@app.route("/user_login",methods = ['GET', 'POST'])
def user_login():
    msg=None
    if request.method == 'POST':
        n = request.form['uname']
        g = request.form['pass']
        n1=str(n)
        g1=str(g)
        q = "SELECT * from user_details where email='" + str(n1) + "' and password='" + str(g1) + "'"
        data = mm.select_login(q)
        if (data=="no"):

            return render_template('user.html',flash_message=True,data="Failed")
        else:

            msg='Success'
            session['user'] =n
            items = mm.select_direct_query(
                "select username,aadhar_number,pan_number from user_details where email='" + str(n) + "'")
            for x in items:
                username = x[0]
                aadhar_number = x[1]
                pan_number = x[2]
                session['username'] = username
                session['aadhar_number'] = aadhar_number
                session['pan_number'] = pan_number
            return user_home()
    return render_template('user.html',error=msg)

@app.route("/bank_login",methods = ['GET', 'POST'])
def bank_login():
    msg=None
    if request.method == 'POST':
        n = request.form['uname']
        g = request.form['pass']
        n1=str(n)
        g1=str(g)
        # /print(n1)
        # /print(g1)
        q=("SELECT * from bank_details where username='" + str(n1) + "' and password='" + str(g1) + "'")
        data=mm.select_direct_query(q)
        data=len(data)
        if data==0:
            return render_template('bank_login.html',flash_message=True,data="Failed")
        else:
            msg='Success'
            session['user'] =n
            return render_template('bank_home.html',sid=n)
    return render_template('bank_login.html',error=msg)

@app.route("/user_home")
def user_home():
    uname = session['user']
    items = mm.select_direct_query("select username,aadhar_number,pan_number from user_details where email='" + str(uname) + "'")
    for x in items:
        username = x[0]
        aadhar_number = x[1]
    return render_template('user_home.html',username=username,aadhar_number=aadhar_number)

@app.route("/user_register", methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']
        gender = request.form['select']
        aadhar_number = request.form['aadhar_number']
        pan_number = request.form['pan_number']
        city = request.form['city']
        pincode = request.form['pincode']
        state = request.form['state']
        maxin = mm.find_max_id("user_details")
        qq = "insert into user_details values('" + str(maxin) + "','" + str(name) + "','" + str(contact) + "','" + str(
            email) + "','" + str(address) + "','" + str(username) + "','" + str(password) + "','" + str(aadhar_number) + "','" \
             + str(pan_number) + "','" + str(city) + "','" + str(pincode) + "','" + str(state) + "','0','"+str(gender)+"')"
        result = mm.insert_query(qq)
        if (result == 1):
            return render_template('user.html',flash_message=True,data="Success")
        else:
            return render_template('user_register.html')
        return render_template('user_register.html', msg="Success")
    else:
        return render_template('user_register.html')
    return render_template('user_register.html')

@app.route("/bank_register", methods=['GET', 'POST'])
def bank_register():
    if request.method == 'POST':
        bank_name = request.form['bank_name']
        ifsc = request.form['ifsc']
        branch = request.form['branch']
        address = request.form['address']
        state = request.form['state']
        country = request.form['country']
        username = request.form['username']
        password = request.form['password']
        maxin = mm.find_max_id("bank_details")
        qq = "insert into bank_details values('" + str(maxin) + "','" + str(bank_name) + "','" + str(ifsc) + "','" + str(
                branch) + "','" + str(address) + "','" + str(state) + "','" + str(country) + "','" + str(username) + "','" + str(password) + "','0','0')"
        result = mm.insert_query(qq)

        if (result == 1):
            return render_template('bank_login.html', msg="Success")
        else:
            return render_template('bank_register.html')
    return render_template('bank_register.html')

@app.route("/user_create_account", methods=['GET', 'POST'])
def user_create_account():
    data=mm.select_direct_query("select username from bank_details")
    uname=session['user']
    items=mm.select_direct_query("select username,aadhar_number,pan_number from user_details where email='"+str(uname)+"'")
    for x in items:
        username=x[0]
        aadhar_number=x[1]
        pan_number=x[2]
        session['username']=username
        session['aadhar_number']=aadhar_number
        session['pan_number']=pan_number
    if request.method == 'POST':
        bank = request.form['select']
        aadhar_no = request.form['aadhar_no']
        pan_no = request.form['pan_no']
        opening_balance = request.form['opening_balance']
        maxin = mm.find_max_id("account_details")
        qq = "insert into account_details values('" + str(maxin) + "','" + str(uname) + "','" + str(
            bank) + "','" + str(
            aadhar_no) + "','" + str(pan_no) + "','" + str(opening_balance) + "','0','0')"
        result = mm.insert_query(qq)
        if (result == 1):
            return render_template('user_home.html')
    return render_template('user_create_account.html',items=data,username=username,aadhar_number=aadhar_number,pan_number=pan_number,opening_balance='5000')

@app.route("/admin_home")
def admin_home():
    return render_template('admin_home.html')

@app.route("/user_deposit",methods = ['GET', 'POST'])
def user_deposit():
    user=session['user']
    q=("SELECT DISTINCT bank from account_details where user='" + str(user) + "'")
    data=mm.select_direct_query(q)
    username=session['username']
    aadhar_number=session['aadhar_number']
    pan_number=session['pan_number']
    if request.method == 'POST':
        bank = request.form['bank']
        amount = request.form['amount']
        qry1=mm.select_direct_query("select opening_balance	 from  account_details where user='"+str(user)+"' and bank='"+str(bank)+"'")
        old_balance=qry1[0][0]
        new_balance=int(old_balance)+int(amount)
        date_object = datetime.date.today()
        arr=random.randint(10000,100000)
        d1=re.sub(r'[^\w]', '', str(date_object)+str(arr))
        plain_text=(bank+""+str(amount)+""+str(arr)+""+str(d1))
        ddd = split_and_store()
        chyper_text=ddd.encrypt(plain_text,1)
        ddd.split_file(chyper_text,(str(d1)))
        result=mm.insert_query("update  account_details set opening_balance='"+str(new_balance)+"' where user='"+str(user)+"' and bank='"+str(bank)+"'")
        result1=mm.insert_query("insert into   mini_statement  values ('"+str(user)+"','"+str(bank)+"','"+str(amount)+"','"+str(aadhar_number)+"','"+str(pan_number)+"','"+str(date_object)+"','Deposit','0','ok')")
    return render_template('user_deposit.html',items=data)

@app.route("/user_withdraw",methods = ['GET', 'POST'])
def user_withdraw():
    user=session['user']
    q=("SELECT DISTINCT bank from account_details where user='" + str(user) + "'")
    data=mm.select_direct_query(q)
    username=session['username']
    aadhar_number=session['aadhar_number']
    pan_number=session['pan_number']
    if request.method == 'POST':
        bank = request.form['bank']
        amount = request.form['amount']
        qry1=mm.select_direct_query("select opening_balance	 from  account_details where user='"+str(user)+"' and bank='"+str(bank)+"'")
        old_balance=qry1[0][0]
        a1=int(old_balance)
        b1=int(amount)
        if(a1>=b1):
            new_balance = int(old_balance) - int(amount)
            date_object = datetime.date.today()
            date_object = datetime.date.today()

            arr = random.randint(10000, 100000)
            d1 = re.sub(r'[^\w]', '', str(date_object) + str(arr))

            plain_text = (bank + "" + str(amount) + "" + str(arr) + "" + str(d1))
            # plain_text = (bank + "" + amount)
            ddd = split_and_store()
            chyper_text = ddd.encrypt(plain_text, 1)
            ddd.split_file(chyper_text, (str(d1)))
            result = mm.insert_query(
                "update  account_details set opening_balance='" + str(new_balance) + "' where user='" + str(
                    user) + "' and bank='" + str(bank) + "'")
            result1 = mm.insert_query(
                "insert into   mini_statement  values ('" + str(user) + "','" + str(bank) + "','" + str(
                    amount) + "','" + str(aadhar_number) + "','" + str(pan_number) + "','" + str(
                    date_object) + "','Withdraw','0','ok')")
            return render_template('user_withdraw.html', items=data,message='Success')
        else:
            return render_template('user_withdraw.html',items=data,message='Low Balance')
    return render_template('user_withdraw.html',items=data)

@app.route("/user_transcation",methods = ['GET', 'POST'])
def user_transcation():
    user=session['user']
    q=("SELECT DISTINCT bank from account_details where user='" + str(user) + "'")
    data=mm.select_direct_query(q)
    username=session['username']
    aadhar_number=session['aadhar_number']
    pan_number=session['pan_number']
    if request.method == 'POST':
        bank = request.form['bank']
        amount = request.form['amount']
        receiverid=request.form['receiver']
        qry1=mm.select_direct_query("select opening_balance	 from  account_details where user='"+str(user)+"' and bank='"+str(bank)+"'")
        old_balance=qry1[0][0]
        a1=int(old_balance)
        b1=int(amount)
        if(a1>=b1):
            new_balance = int(old_balance) - int(amount)
            date_object = datetime.date.today()
            arr = random.randint(10000, 100000)
            d1 = re.sub(r'[^\w]', '', str(date_object) + str(arr))
            plain_text = (bank + "" + str(amount) + "" + str(arr) + "" + str(d1))
            ddd = split_and_store()
            chyper_text = ddd.encrypt(plain_text, 1)
            import time
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            x = current_time.split(":")
            tmp_id = str(x[0]) + str(x[1]) + str(x[2])
            ddd.split_file(chyper_text, (str(tmp_id)))
            result1 = mm.insert_query("insert into   mini_statement  values ('" + str(user) + "','" + str(bank) + "','" + str(amount) + "','" + str(aadhar_number) + "','" + str(pan_number) + "','" + str(date_object) + "','Debit','"+str(receiverid)+"','"+str(tmp_id)+"')")
            qry1 = mm.select_direct_query("select opening_balance	 from  account_details where user='" + str(receiverid) + "'")
            old_balance = qry1[0][0]
            new_balance = int(old_balance) + int(amount)
            date_object = datetime.date.today()
            result1 = mm.insert_query("insert into   mini_statement  values ('" + str(receiverid) + "','" + str(bank) + "','" + str(amount) + "','" + str(aadhar_number) + "','" + str(pan_number) + "','" + str(date_object) + "','Credit','"+str(user)+"','"+str(tmp_id)+"')")
            return render_template('user_transcation.html', items=data,message='Success')
        else:
            return render_template('user_transcation.html',items=data,message='Low Balance')
    return render_template('user_transcation.html',items=data)

@app.route("/user_received",methods = ['GET', 'POST'])
def user_received():
    user=session['user']
    q=("SELECT * from mini_statement where user='" + str(user) + "' and  verification NOT IN ('ok') and status='Credit'")
    data=mm.select_direct_query(q)
    return render_template('user_received.html',items=data)

@app.route("/user_received_1/<string:id>",methods = ['GET', 'POST'])
def user_received_1(id):
    pp=split_and_store()
    rrr=pp.match_file(file=str(id))
    if rrr=="refund":
        mm.insert_query("update mini_statement set status='Credit Refund',verification='ok' where verification='"+str(id)+"' and status='Credit'")
        mm.insert_query("update mini_statement set status='Debit Refund',verification='ok' where verification='"+str(id)+"' and status='Debit'")
    else:
        data=mm.select_direct_query("select * from mini_statement where verification='"+str(id)+"'")
        user =data[0][0]
        bank =data[0][1]
        amount =data[0][2]
        receiverid =data[0][7]
        aadhar_number=data[0][3]
        pan_number=data[0][4]
        qry1 = mm.select_direct_query( "select opening_balance	 from  account_details where user='" + str(user) + "' and bank='" + str(bank) + "'")
        old_balance = qry1[0][0]
        a1 = int(old_balance)
        b1 = int(amount)
        if (a1 >= b1):
            new_balance = int(old_balance) - int(amount)
            date_object = datetime.date.today()
            arr = random.randint(10000, 100000)
            d1 = re.sub(r'[^\w]', '', str(date_object) + str(arr))
            plain_text = (bank + "" + str(amount) + "" + str(arr) + "" + str(d1))
            ddd = split_and_store()
            chyper_text = ddd.encrypt(plain_text, 1)
            import time
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            x = current_time.split(":")
            tmp_id = str(x[0]) + str(x[1]) + str(x[2])
            ddd.split_file(chyper_text, (str(tmp_id)))
            result = mm.insert_query("update  account_details set opening_balance='" + str(new_balance) + "' where user='" + str(user) + "' and bank='" + str(bank) + "'")
            qry1 = mm.select_direct_query("select opening_balance	 from  account_details where user='" + str( receiverid) + "'")
            old_balance = qry1[0][0]
            new_balance = int(old_balance) + int(amount)
            date_object = datetime.date.today()
            result = mm.insert_query("update  account_details set opening_balance='" + str(new_balance) + "' where user='" + str(receiverid) + "'")
            mm.insert_query("update mini_statement set verification='ok' where verification='" + str(id) + "' and status='Credit'")
            mm.insert_query( "update mini_statement set verification='ok' where verification='" + str( id) + "' and status='Debit'")
            return render_template('user_transcation.html', items=data, message='Success')
    return render_template('user_received.html')

@app.route("/user_mini_statement",methods = ['GET', 'POST'])
def user_mini_statement():
    user=session['user']
    q=("SELECT  bank,amount,date_object,status,report from mini_statement where user='" + str(user) + "'")
    data=mm.select_direct_query(q)
    return render_template('user_mini_statement.html',items=data)

@app.route("/admin_user",methods = ['GET', 'POST'])
def admin_user():
    q=("SELECT  id,name,contact,email,address,report from user_details")
    data=mm.select_direct_query(q)
    return render_template('admin_user.html',items=data)

@app.route("/admin_bank",methods = ['GET', 'POST'])
def admin_bank():
    q=("SELECT bank_name,ifsc,branch,address,state,country	 from bank_details")
    data=mm.select_direct_query(q)
    return render_template('admin_bank.html',items=data)

@app.route("/admin_bribery",methods = ['GET', 'POST'])
def admin_bribery():
    q=("SELECT DISTINCT user FROM account_details")
    data=mm.select_direct_query(q)
    items=[]
    for x in data:
        qq=("select SUM(opening_balance) from account_details where user='" + str(x[0]) + "'")
        total = (mm.select_direct_query(qq))
        if (int(total[0][0]))>=0:
            q2 = "select aadhar_no,pan_no from account_details where user='" + str(x[0]) + "'"
            details = mm.select_direct_query(q2)
            items.append([x[0], total[0][0], details[0][0], details[0][1]], )
    return render_template('admin_bribery.html',items=items)

@app.route("/bank_home",methods = ['GET', 'POST'])
def bank_home():
    return render_template('bank_home.html')

@app.route("/bank_user",methods = ['GET', 'POST'])
def bank_user():
    q=("SELECT id,name,contact,email,address,aadhar_number,pan_number,city,pincode,state from user_details")
    data=mm.select_direct_query(q)
    return render_template('bank_user.html',items=data)

@app.route("/bank_account_info",methods = ['GET', 'POST'])
def bank_account_info():
    n=session['user']
    q=("SELECT id,user,bank,aadhar_no,pan_no,opening_balance from account_details where bank='"+ str(n) +"'")
    data=mm.select_direct_query(q)
    return render_template('bank_account_info.html',items=data)

@app.route("/bank_transaction",methods = ['GET', 'POST'])
def bank_transaction():
    n=session['user']
    q=("SELECT * from mini_statement where bank='"+ str(n) +"'")
    data=mm.select_direct_query(q)
    return render_template('bank_transaction.html',items=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, use_reloader=True,port=4550)

