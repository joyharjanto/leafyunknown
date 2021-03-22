from flask import Flask, render_template, request, jsonify
import requests
import pprint
import sqlite3 as sql

app = Flask(__name__)

joys_key = '0gTcQtweKZPOZFF1MUZL5Uh71zuQHH3AU6gV3y7O'

# conn = sql.connect('api.db') #databse is called api
# conn.execute('CREATE TABLE results (id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, event_id INTEGER)')
# conn.close()

@app.route('/')
def home():
    # try:
    url = 'https://api.fda.gov/food/enforcement.json?api_key='+joys_key+'&search=distribution_pattern:%22nationwide%22&limit=5'
    r = requests.get(url).json()

    with sql.connect("api.db") as con:
        cur = con.cursor()
        for i in range(0,len(r['results'])):
            cur.execute("INSERT INTO results (city, event_id) VALUES (?,?)",(r['results'][i]['city'],r['results'][i]['event_id']))
        con.commit()
        print("successfully added data")
    return r
    # except:
    #     return "fail"

@app.route('/list')
def list():
   con = sql.connect("api.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("select * from results")

   rows = cur.fetchall();
   return render_template("list.html", rows = rows)

@app.route('/update')
def update_data():
    con = sql.connect("api.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("UPDATE results SET city = 'LONDON' where id = 1")
    con.commit()
    print("successs update")
    return "success"

@app.route('/delete')
def delete_data():
    con = sql.connect("api.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    print("not far enough")
    cur.execute("DELETE FROM results WHERE id=?", (11,))
    cur.execute("DELETE FROM results WHERE id=?", (12,))
    cur.execute("DELETE FROM results WHERE id=?", (13,))
    con.commit()
    print("Can commit")
    return "successfully deleted"

@app.route('/manualinsert')
def manually_insert():
    con = sql.connect("api.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("INSERT INTO results (city, event_id) VALUES (?,?)",("London","75097"))
    con.commit()
    return "successfully manually inserted"

@app.route('/api/resources', methods=['GET'])
def api_filter():
    query_params = request.args
    print(query_params)
    id = query_params.get('id')
    city = query_params.get('city')
    event_id = query_params.get('event_id')
    print(id)
    print(city)
    print(event_id)

    to_filter = []

    query = 'SELECT * FROM results WHERE'

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if city:
        query += ' city=? AND'
        to_filter.append(city)
    if event_id:
        query += ' event_id=? AND'
        to_filter.append(event_id)

    query = query[:-4]
    print("this far")
    with sql.connect("api.db") as con:
        # con.row_factory = sql.Row
        cur = con.cursor()
        result = cur.execute(query, to_filter).fetchall()
        print(result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
