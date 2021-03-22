from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
# comment because tables have been created once before, making of database
# conn = sqlite3.connect('api.db') #databse is called api
# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
# print("Table created successfully");
# conn.close()
# print("succs")


@app.route('/')
def hello():
    return render_template("student.html")

@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    msg = "yup"
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

         #updating data
            conn = sqlite3.connect("api.db")
            if(sqlite3.connect("api.db")):
                print("connected")
            else:
                print("fake news")
            #actual moves through the database
            with sqlite3.connect("api.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin))
                con.commit()
                msg = "Record successfully added"
                print("done trying")
        except:
            print("except")
            con.rollback() #undoing all changes
            msg = "error in insert operation"

        finally: #done regardless
            print("finally")
            return render_template("result.html",msg = msg)
            con.close()

@app.route('/list')
def list():
   con = sqlite3.connect("api.db")
   con.row_factory = sqlite3.Row

   cur = con.cursor()
   cur.execute("select * from students")

   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == "__main__":
    app.run(debug=True)
