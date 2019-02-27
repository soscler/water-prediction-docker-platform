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
session.execute("""
        CREATE TABLE IF NOT EXISTS tempgallons (
            temp_id bigint,
            temp bigint,
            gallons bigint,
            PRIMARY KEY (temp_id)
        )
        """)
session.execute(""" INSERT INTO tempgallons (temp_id, temp ,gallons) VALUES(1,2,4) """)        


@app.route("/")
def post_to_front():
    rows = session.execute('SELECT * FROM tempgallons')
    pulled =[]
    for row in rows:
        print(row)
        each_row ={
            'temp_id':row.temp_id,
            'temp':row.temp,
            'Gallons': row.gallons
        }
        pulled.append(each_row)
    msg=jsonify({'result': pulled})
    return render_template("index.html",msg=msg.response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int("5000"))