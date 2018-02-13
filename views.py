from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
import sqlite3 as sql
import sqlite3

engine = create_engine('sqlite:///tutorial.db', echo=True)
 
app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
	return render_template('home.html')

	



 
@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("student.html",msg = msg)
         con.close()



@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row


   cur = con.cursor()
   cur.execute("select * from students")
   

   rows = cur.fetchall();
   return render_template("list.html",rows = rows)




@app.route('/delete/<int:delete_id>')
def delete_entry(delete_id):
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   delete_id=int(delete_id)
   cur.execute("delete from students where id=?", (delete_id,))
   con.commit()
   return redirect("http://194.135.89.2:4000/list")
   


@app.route('/edit/<int:edit_id>')
def edit_entry(edit_id):
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   edit_id=int(edit_id)
   cur.execute("select * from students where id=?", (edit_id,))
   #con.commit()

   rows = cur.fetchall();
   return render_template("edit.html",rows = rows)


@app.route('/update/<int:update_id>',  methods=['POST'])
def update_entry(update_id):
   
   nm = request.form['nm']
   addr = request.form['add']
   city = request.form['city']
   pin = request.form['pin']
   

   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()

   update_id=int(update_id)

   cur.execute("update students set name=?, addr=?, city=?, pin=? where id=?", (nm, addr, city, pin, update_id,))
   con.commit()
   rows = cur.fetchall();
   return redirect("http://194.135.89.2:4000/list")


@app.route('/student')
def student():
   return render_template("student.html")


 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
