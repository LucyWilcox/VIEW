import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import time
import random
# import config as con                                              fig

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World! The app is up!'

@app.route('/todo/api/v1.0/currid', methods=['GET'])
def get_id_v1():
	# database_URI = config.DATABASE_URI
	database_URI = os.environ['DATABASE_URI']
	conn = psycopg2.connect(database_URI)
	curr = conn.cursor()
	curr.execute("SELECT * FROM CurrentId;")
	curr_id = curr.fetchone()[1]
	print curr_id
	conn.commit()
	curr.close()
	conn.close()
	return jsonify({'currid': curr_id}), 200

@app.route('/todo/api/v2.0/currid/images/<numimages>', methods=['GET'])
def get_id_v2(numimages):
	# database_URI = config.DATABASE_URI
	database_URI = os.environ['DATABASE_URI']
	conn = psycopg2.connect(database_URI)
	curr = conn.cursor()
	current_time = time.time() * 1000
	current_day = time.gmtime(current_time / 1000)[2]
	curr.execute("SELECT * FROM CurrentId;")
	result = curr.fetchone()
	curr_id = result[1]
	last_time = result[2]
	last_day = time.gmtime(last_time / 1000)[2]
	if current_day != last_day:
		curr_id = random.randint(0, int(numimages) - 1)
		new_day_sql = "UPDATE CurrentId SET curr_id = %s WHERE id = 1" %(curr_id)
		curr.execute(new_day_sql)
	update_time = "UPDATE CurrentId SET time = %s WHERE id = 1" %(current_time)
	curr.execute(update_time)
	conn.commit()
	curr.close()
	conn.close()
	return jsonify({'currid': curr_id}), 200

@app.route('/todo/api/v1.0/currid', methods=['POST'])
def post_id():
	# database_URI = config.DATABASE_URI
	database_URI = os.environ['DATABASE_URI']
	if not request.json:
		print "could not find request.json"
	if not 'newid' in request.json:
		print "no newid in request.json"
	print request.json
	conn = psycopg2.connect(database_URI)
	curr = conn.cursor()
	curr_id = request.json['newid']
	print curr_id
	sql = "UPDATE CurrentId SET curr_id = %s WHERE id = 1" %(curr_id)
	print sql
	curr.execute(sql)
	conn.commit()
	curr.close()
	conn.close()
	return jsonify({'currid': curr_id}), 201

@app.route('/todo/api/v3.0/allurls', methods=['GET'])
def get_urls():
	# database_URI = config.DATABASE_URI
	database_URI = os.environ['DATABASE_URI']
	conn = psycopg2.connect(database_URI)
	curr = conn.cursor()
	curr.execute("SELECT image FROM images;")
	all_urls = []
	for row in curr:
		all_urls.append(row[0])
	conn.commit()
	curr.close()
	conn.close()
	return jsonify({'allurls': all_urls}), 200

@app.route('/todo/api/v3.0/allurls', methods=['POST'])
def post_urls():
	# database_URI = config.DATABASE_URI
	database_URI = os.environ['DATABASE_URI']
	if not request.json:
		print "could not find request.json"
	if not 'allurls' in request.json:
		print "no allurls in request.json"
	print request.json
	conn = psycopg2.connect(database_URI)
	curr = conn.cursor()
	sql = "TRUNCATE Images;"
	curr.execute(sql)
	conn.commit()
	all_urls = request.json['allurls']
	all_urls = all_urls.split() 
	# please seperate url with a space
	for i in all_urls:
		sql = "INSERT INTO Images VALUES (%i, '%s');" %(1, i)
		print sql
		curr.execute(sql)
		conn.commit()
	curr.close()
	conn.close()
	return jsonify({'allurls': all_urls}), 201

@app.route('/todo/api/v3.0/currurl', methods=['GET'])
def get_url():
	# database_URI = config.DATABASE_URI
	database_URI = os.environ['DATABASE_URI']
	conn = psycopg2.connect(database_URI)
	curr = conn.cursor()
	curr.execute("SELECT curr_url FROM CurrentId;")
	curr_url = curr.fetchone()
	print curr_url
	conn.commit()
	curr.close()
	conn.close()
	return jsonify({'curr_url': curr_url}), 200

@app.route('/todo/api/v3.0/currurl', methods=['POST'])
def post_url():
	# database_URI = config.DATABASE_URI
	database_URI = os.environ['DATABASE_URI']
	if not request.json:
		print "could not find request.json"
	if not 'currurl' in request.json:
		print "no currurl in request.json"
	# if not 'nexturl' in request.json:
	# 	print "no nexturl in request.json"
	print request.json
	conn = psycopg2.connect(database_URI)
	curr = conn.cursor()
	curr_url = request.json['currurl']
	curr_url = "'" + curr_url + "'"
	sql = "UPDATE CurrentId SET curr_url = %s WHERE id = 1" %(curr_url)
	curr.execute(sql)
	# next_url = request.json['nexturl']
	# next_url = "'" + next_url + "'"
	# sql = "UPDATE CurrentId SET next_url = %s WHERE id = 1" %(next_url)
	# print sql
	# curr.execute(sql)
	conn.commit()
	curr.close()
	conn.close()
	return jsonify({'currurl': curr_url}), 201

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port)

