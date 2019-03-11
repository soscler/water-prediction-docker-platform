from flask import Flask,render_template,url_for,jsonify
from cassandra.cluster import Cluster
import os

KEYSPACE = "weatherwater"
app = Flask(__name__)

#Connecting to cassandra
cluster = Cluster([os.environ.get('CASSANDRA_PORT_9042_TCP_ADDR')], port=int(os.environ.get('CASSANDRA_PORT_9042_TCP_PORT')))

session = cluster.connect()

# Init the database
session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
        """ % KEYSPACE)
session.set_keyspace(KEYSPACE)
# session.execute("""
#         CREATE TABLE IF NOT EXISTS tempgallons (
#             temp_id bigint,
#             temp bigint,
#             gallons bigint,
#             PRIMARY KEY (temp_id)
#         )
#         """)
session.execute("""
        CREATE TABLE IF NOT EXISTS testpredictions (
            id bigint,
            yyyymmdd timestamp,
            hh bigint,
            gallons float,
            prediction float,
            PRIMARY KEY (id,yyyymmdd)
        )
        """)        
# session.execute(""" INSERT INTO testpredictions (id, year, hour , gallons, predicted_gallons) VALUES(uuid(),20190308,05,1.45, 0.96) """)        


@app.route("/")
def post_to_front():
    rows = session.execute('SELECT * FROM testpredictions')
    pulled =[]
    for row in rows:
        print(row)
        each_row ={
            'id':row.id,
            'Time': row.hh,
            'year':row.yyyymmdd,
            'Gallons': row.gallons,
            'predicted_gallons': row.prediction
        }
        pulled.append(each_row)
    # msg=jsonify({'result': pulled})
    return render_template("index.html",msg=pulled)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int("5000"))