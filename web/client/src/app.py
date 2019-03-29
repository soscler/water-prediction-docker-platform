from flask import Flask,render_template,url_for,jsonify
from cassandra.cluster import Cluster
import os
import datetime

KEYSPACE = "weatherwater"
app = Flask(__name__)

#Connecting to cassandra
cluster = Cluster([os.environ.get('CASSANDRA_PORT_9042_TCP_ADDR')], port=int(os.environ.get('CASSANDRA_PORT_9042_TCP_PORT')))
print(os.environ.get('CASSANDRA_PORT_9042_TCP_ADDR'))
session = cluster.connect()

# Init the database
session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
        """ % KEYSPACE)
session.set_keyspace(KEYSPACE)

session.execute("""
        CREATE TABLE IF NOT EXISTS testpredictions (
            id bigint,
            yyyymmdd timestamp,
            hh bigint,
            temperature float,
            gallons float,
            prediction float,
            PRIMARY KEY (yyyymmdd,id)
        )
        """)              
session.execute("""
    CREATE TABLE IF NOT EXISTS rmse(
        date string,
        rmse float,
        PRIMARY KEY(date)
    )
""")

# session.execute("""
#     ALTER TABLE testpredictions ADD temperature float
# """)


@app.route("/")
def post_to_front():
    rows = session.execute('SELECT id,yyyymmdd,MAX(prediction) as prediction,hh,temperature FROM testpredictions GROUP BY yyyymmdd;')
    pulled =[]
    for row in rows:
        print(row)
        each_row ={
            'id':row.id,
            'Time':row.hh,
            'year':row.yyyymmdd.strftime("%m/%d/%Y"),
            'predicted_gallons':row.prediction,
            "temperature": row.temperature
        }
        pulled.append(each_row)
    # msg=jsonify({'result': pulled})
    return render_template("index.html",msg=pulled)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=int("5000"))