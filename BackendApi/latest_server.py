#Flask is a micro web application framework written in Python
from flask import *
import json
import uuid
import csv
import MySQLdb
#from flask.ext.cors import CORS
import random
import string

import time
from threading import Timer
import requests

from LoadBalance import *

#create balancer object
b=Balancer()
timer_dict=dict()

def dict_factory(cursor, row):
	d = {}
	for index, col in enumerate(cursor.description):
		d[col[0]] = row[index]
	return d

db_config = {}
#db.config->file having username and password
with open('db.config') as f:
	db_config = {t.split(':')[0] : t.split(':')[1] for t in f.read().split('\n')}

#printing configuration parameters
print db_config 
#Obtaining connection to mysql database(Excavator)
db                    = MySQLdb.connect(
							host="localhost",
							user=db_config['user'],
							passwd=db_config['password'],
							db="Excavator"
						)
db.row_factory        = dict_factory

#To obtain cursor object
cursor                = db.cursor()
#cursor is cursor object of Excavator database
#Obtaining connection to mysql database(Data)
client_db             = MySQLdb.connect(
							host="localhost",
							user=db_config['user'],
							passwd=db_config['password'],
							db="Data"
						)
client_db.row_factory = dict_factory
client_cursor         = client_db.cursor()
#client_cursor is cursor object of Data database

client_db.set_character_set('utf8')
client_cursor.execute('SET NAMES utf8;') 
client_cursor.execute('SET CHARACTER SET utf8;')
client_cursor.execute('SET character_set_connection=utf8;')

#To start up with flask
app                   = Flask(__name__)
app.secret_key        ='something'
#cors                  = CORS(app)
app.config['DEBUG']   = True

app.config.from_object(__name__)


@app.route('/api/user/signup', methods=['GET'])
	
def api_user_signup():

	'''
	Sign up api which is used by new users
	Input:
		username
		password
	Output:
		status ("success"/"fail")
		if("success") => token
		if("fail") => reason (an err msg is displayed to user)
	What it does:
	Adds an entry to users table and returns token,if it's not succesful reason is informed to user
	'''


	if('username' in request.args and 'password' in request.args):
		#fetching parameters passed through get request
		username = request.args['username']
		password = request.args['password']

		print username
		print password
		print "++++++++++"

		if(cursor.execute('select * from user where username = %s', (username,)) == 0):
			token  = ''.join([random.choice(string.ascii_lowercase) for i in range(20)])
			# user = User(username = username, password = password, token = token)
			cursor.execute('insert into user values(%s, %s, %s)', (username, password, token))
			db.commit()
			return jsonify({
				'status' : 'success',
				'token' : token
			})
		else:
			return jsonify({
				'status' : 'error',
				'reason' : 'username is already taken'
			})
	else:
		print list(request.args)
		return jsonify({
			'status' : 'error',
			'reason' : 'Server communication error. Please Try again'
		})


		
		
	
@app.route('/api/user/signin', methods=['GET'])	
def api_user_signin():
	'''
	Sign in api which is used by existing users
	Input:
		username
		password
	returns:
		status ("success"/"fail")
		if("success") => token
		if("fail") => reason (an error msg is displayed to usr)
	What it does:
	checks if valid username and password and returns token
	'''	


	if('username' in request.args and 'password' in request.args):
		username = request.args['username']
		password = request.args['password']
		#Fetching data from users table
		if(cursor.execute('select token from user where username = %s and password = %s', (username, password)) == 1):#to check whether the user exists
			print "in if"
			return jsonify({
				'status' : 'success',
				'token' : cursor.fetchall()[0][0]
			})
		else:
			cursor.fetchall()
			return jsonify({
				'status' : 'error',
				'reason' : 'Please check your username and password' #If user exists 
			})
	else:
		return jsonify({
			'status' : 'error',
			'reason' : 'Server communication error, Please try again'
		})
def set_timer(url="",columns = "",rules ="",table_id=""):
	scheduler(url,columns,rules,table_id)
	timer_id = Timer(1000,set_timer,(url,columns,rules,table_id))
	global timer_dict
	timer_dict['table_id']=timer_id
	timer_id.start()
	print "done with timer_id"
	scheduler(url,columns,rules,table_id)	


def scheduler(url="",columns="",rules="",table_id=""):
	#b.request() #returns the json object .
	#json_str = b.request(url,columns,rules)
	print("in scheduler")
	json_str=json_str={u'status': u'SUCCESS', u'data': [{u'something': u'Where do investigators throw away their medical gloves after examining a body if there is no garbage bin nearby?'}, {u'something': u'RadiantMan'}, {u'something': u'/r/AskReddit'}, {u'something': u'3 comments'}, {u'something': u''}, {u'something': u'Chinese Company Says It Never Planned a \u2018Thugs for Hire\u2019 App'}, {u'something': u'Ripclawe'}, {u'something': u'/r/nottheonion'}, {u'something': u'comment'}, {u'something': u'Trouble choosing a college due to tuition costs.'}, {u'something': u'PumaConnection'}, {u'something': u'/r/personalfinance'}, {u'something': u'2 comments'}, {u'something': u''}, {u'something': u'Fast and Furious 8 on April 14, 2017'}, {u'something': u'ray_marcos'}, {u'something': u'/r/movies'}, {u'something': u'comment'}, {u'something': u'[Serious] How to ask a girl out without being afraid of rejection?'}, {u'something': u'shallowline'}, {u'something': u'/r/AskReddit'}, {u'something': u'11 comments'}, {u'something': u'The best defense a girl has against an unwanted dick pic, is to send back a different dick pic.'}, {u'something': u'typing'}, {u'something': u'/r/Showerthoughts'}, {u'something': u'7 comments'}, {u'something': u'Car Auto Loan vs Dealership financing (Canada)'}, {u'something': u'bookfancier69'}, {u'something': u'/r/personalfinance'}, {u'something': u'comment'}, {u'something': u'What statement or saying do you absolutely hate, but is also absolutely true?'}, {u'something': u'DarkChurro'}, {u'something': u'/r/AskReddit'}, {u'something': u'9 comments'}, {u'something': u'Debt?'}, {u'something': u'Tonberry_Cherry'}, {u'something': u'/r/personalfinance'}, {u'something': u'2 comments'}, {u'something': u''}, {u'something': u"25 incredible images on Hubble telescope's silver jubilee"}, {u'something': u'Tom_JerryToon'}, {u'something': u'/r/space'}, {u'something': u'comment'}, {u'something': u'59 comments'}, {u'something': u''}, {u'something': u"I work in the utility field. Here's an old copper ped and a new fiber ped for comparison."}, {u'something': u'kasmith1244'}, {u'something': u'/r/pics'}, {u'something': u'640 comments'}, {u'something': u''}, {u'something': u'Another American letdown'}, {u'something': u'-dudeomfgstfux-'}, {u'something': u'/r/funny'}, {u'something': u'1322 comments'}, {u'something': u''}, {u'something': u'Otter with otter stuffed animal'}, {u'something': u'MESK1MEN'}, {u'something': u'/r/aww'}, {u'something': u'117 comments'}, {u'something': u''}, {u'something': u'What if Man of Steel was IN COLOR?'}, {u'something': u'stroudwes'}, {u'something': u'/r/movies'}, {u'something': u'897 comments'}, {u'something': u''}, {u'something': u'Octopus hunting a crab'}, {u'something': u'thebigsexy1'}, {u'something': u'/r/gifs'}, {u'something': u'767 comments'}, {u'something': u''}, {u'something': u"TIL: There's a company that takes donations to purchase student loans at pennies on the dollar just to wipe them out and has wiped $32m to date."}, {u'something': u'blowpoptops'}, {u'something': u'/r/todayilearned'}, {u'something': u'70 comments'}, {u'something': u''}, {u'something': u'This sign can not be seen from the street. It sits on a rooftop of a restaurant across from a hospital. You can only see it from the windows of the hospital.'}, {u'something': u'blackjackel'}, {u'something': u'/r/mildlyinteresting'}, {u'something': u'28 comments'}, {u'something': u'Reddit turned me into a hipster. People "hey did you see that thing on the news?" Me "yea I saw it before you on reddit"'}, {u'something': u'Denvermax31'}, {u'something': u'/r/Showerthoughts'}, {u'something': u'208 comments'}, {u'something': u''}, {u'something': u'IamA mediocre comedian Jim Norton AMA!'}, {u'something': u'TheRealJimNorton'}, {u'something': u'/r/IAmA'}, {u'something': u'1822 comments'}, {u'something': u'Ireland set to examine possibility of decriminalizing cannabis'}, {u'something': u'niall558'}, {u'something': u'/r/worldnews'}, {u'something': u'241 comments'}, {u'something': u'ELI5: How do registered sex offenders go to grocery stores and malls etc, where children just are naturally?'}, {u'something': u'ArtistApart'}, {u'something': u'/r/explainlikeimfive'}, {u'something': u'803 comments'}, {u'something': u''}, {u'something': u"Ghost Stories is an anime that was so shitty the American voice actors were told to do whatever they wanted with the script... here's the result..."}, {u'something': u'secksee'}, {u'something': u'/r/videos'}, {u'something': u'1143 comments'}, {u'something': u'GM, Ford, And Others Want to Make Working on Your Own Car Illegal'}, {u'something': u'musicforthedeaf'}, {u'something': u'/r/news'}, {u'something': u'961 comments'}, {u'something': u''}, {u'something': u'My beautiful mom at 18 in 1976'}, {u'something': u'count_olafs'}, {u'something': u'/r/OldSchoolCool'}, {u'something': u'494 comments'}, {u'something': u''}, {u'something': u'LPT: To avoid being scammed by phoney debt collectors, request a "validation notice".'}, {u'something': u'RalphiesBoogers'}, {u'something': u'/r/LifeProTips'}, {u'something': u'641 comments'}, {u'something': u''}, {u'something': u'Louis Theroux: Just been informed by Scientology lawyers that Scientology is working on a documentary about me. Little bit excited; little bit nervous... (2015)'}, {u'something': u'Stevee04'}, {u'something': u'/r/Documentaries'}, {u'something': u'1259 comments'}, {u'something': u'What should the first city on Mars be called?'}, {u'something': u'Static_Storm'}, {u'something': u'/r/AskReddit'}, {u'something': u'3989 comments'}, {u'something': u"90s kids won't get this . . ."}, {u'something': u'sammyslobando'}, {u'something': u'/r/Jokes'}, {u'something': u'1612 comments'}, {u'something': u''}, {u'something': u"Louis Theroux informed that 'Scientology is working on a documentary' about him"}, {u'something': u'here2dare'}, {u'something': u'/r/television'}, {u'something': u'333 comments'}, {u'something': u"A Cooper's hawk found near a Vancouver-area waste transfer station is believed to be the most polluted wild bird in the world, according to a new study. The hawk's liver fat was packed with 197,000 parts per billion of PBDEs \u2014 a chemical used as a flame retardant."}, {u'something': u'drewiepoodle'}, {u'something': u'/r/science'}, {u'something': u'35 comments'}, {u'something': u''}, {u'something': u'Curiosity rover spoted by Mars Reconnaissance Orbiter on April 8, 2015 on the lower slope of Mount Sharp.'}, {u'something': u'Ramambahara'}, {u'something': u'/r/space'}, {u'something': u'821 comments'}, {u'something': u'TIL the first programmers, who wrote programs for the first ever digital computers, were ALL women'}, {u'something': u'lambda_schmambda'}, {u'something': u'/r/TwoXChromosomes'}, {u'something': u'167 comments'}, {u'something': u'TIFU by having a lapse of concentration at a revolving door..'}, {u'something': u'Frankeh'}, {u'something': u'/r/tifu'}, {u'something': u'630 comments'}, {u'something': u''}, {u'something': u'1947 18-Window Frankenstein Buick Hearse'}, {u'something': u'ethan_kahn'}, {u'something': u'/r/creepy'}, {u'something': u'442 comments'}, {u'something': u''}, {u'something': u"Landscape Arch - Devil's Garden - Arches National Park in Utah (1024x1024 | OS | JR Goodwin)"}, {u'something': u'tek0011'}, {u'something': u'/r/EarthPorn'}, {u'something': u'169 comments'}]}

	if(json_str['status']=="SUCCESS"):
		#[{"data": [{"field1": "value1", "field2": "value2"}, {"field1": "value3", "filed2": "value4"}]}] - Assuming the json is in this format
		res          = json_str['data']
		
		row_db_entry = []
		#get the keys (field names of the table)
		keys         = []
		
		for row in res:
			for i in row.keys():
				keys.append((i))
		print(set(keys))
		for row in res:
			new_dict = dict()
			for item in set(keys):
				new_dict[item] =(row[item])
				#print(item,new_dict[item])
			row_db_entry.append(new_dict)
		print("\n\n")	
		print("\n\n")
		values_only = []
		#the list values_only has the attribute values to be inserted into the database
		for row in row_db_entry:
			field_val = row.values()
			values_only.append(field_val)

		
		try:
			attr_with_type = ""
			attr           = ""
			#formulate the sql query to create a table in the user's db
			'''for i in set(keys):
				attr_with_type += (i+" varchar(200), ")
				attr = attr + "," + i 
			attr = attr[1:]
			attr_with_type = attr_with_type + "primary key("+ attr +")"
			sql = "create table if not exists " + table_id + "(" + attr_with_type +")"
			print(sql)

			client_cursor.execute(sql)'''
			#values_only = values_only
			
			num_of_attr = len(values_only[0])
			s           = "%s,"*num_of_attr
			key_string = ""

			key_string = ",".join([str(i) for i in set(keys)])
			#print(key_string)
			#print(num_of_attr,"cudsicidsuh")
			sql         ="insert into "+table_id+"("+key_string+")"+" values (" +s[:-1] +")"
			
			print(sql)
			
			values_only = [i[0] for i in values_only]
			
			for i in values_only:
				try:
					client_cursor.execute(sql,(i,))
					client_db.commit()
				except:
					pass
			
			print("success")
		except:
			print("Table entry already exists")
		#scheduled every 10 seconds right now.
		"""timer_id = Timer(10,scheduler,(url,columns,rules,table_id))
		global timer_dict
		timer_dict['table_id']=timer_id
		timer_id.start()"""
		#return
	else:
		print("unsuccessful")
		#return



@app.route('/api/table/create', methods=['GET'])
def api_table_create():


	'''
	Input:
		table_name
		token
		url
		columns as a string containing ;-seperated values
		rules as a string containing ;-seperated values

	Output:
		success : if table is created and information about table is added appropriately to Excavator database
		error : user already exists or redundant entry of table_name/column
	'''

	

	table_name = request.args['table_name']
	token      = request.args['token']
	url        = request.args['url']
	columns    = request.args['columns']
	rules      = request.args['rules']
	#print(table_name+token+url+columns+rules)
	#creates a unique id for table for each user.
	table_id = token + "_" + table_name;
	
	#user validation
	query_result = cursor.execute("select * from user where token = %s",(token,))
	if(query_result):
		try:
			#Excavator database
			cursor.execute(
				"INSERT INTO tables(table_id, token, table_name, table_url) VALUES(%s,%s,%s,%s)", (
					table_id,
					token,
					table_name,
					url
				)
			)


			columns = columns.split(';') #list of column_names
			rules   = rules.split(';')	#list of rules corresponding to columns

			for i in range(len(columns)):
				cursor.execute(
					"INSERT INTO columns(table_id, column_name, column_rule) VALUES(%s,%s,%s)", (
						table_id,
						columns[i],
						rules[i]
					)
				)
				

			#Data database
			query = "CREATE TABLE " + table_id 
			fields_type = list()
			fields = list()
			for i in columns:
				fields_type.append(i + " VARCHAR(767)")
				fields.append(i)

			query += "(" + ','.join(fields_type) + ", PRIMARY KEY(" + ','.join(fields) + "))"
			client_cursor.execute(query)
			set_timer(url,columns,rules,table_id)
			db.commit()
			client_db.commit()
			return jsonify({"status" : "Success"})
		
		except:
			reason_status = "Table or column already exists"
			return jsonify({"status" : "Failure","reason" : reason_status})

	else:
		#no user 
		reason_status = "User not found"
		return jsonify({"status" : "Failure","reason" : reason_status})

	


@app.route('/api/table/show', methods = ['GET'])
def api_table_show():
	'''
	Input:
		table_id
		token
	
	Output:
		success : Returns details of the table with table_id for user - token:
					Name of the table
					URL where the data of the table is scraped
					List of columns and their associated rules
		error : user or table not found
	'''
	
	token    = request.args['token']
	table_id = request.args['table_id']

	query_result = cursor.execute("select * from user where token = %s",(token,))
	if(query_result):
		#To fetch details from tables table
		table_result = cursor.execute(
			"SELECT table_url, table_name FROM tables where table_id = (%s)",(
				table_id,
			)
		)
		if(table_result):

			url_name             = cursor.fetchall()
			
			result               = dict()
			result['url']        = url_name[0][0]
			result['table_name'] = url_name[0][1]
		
			cursor.execute("select column_name,column_rule from columns where table_id = %s",(table_id,))
	
			column_names_rules = cursor.fetchall()
			
			result['columns']  = list() #contains a list : Each item in the list is a dictionary with column_name and column_rule
			for i in column_names_rules:
				cols           = dict()
				cols['column'] = i[0]
				cols['rule']   = i[1]
				result['columns'].append(cols)
			
			result = json.dumps(result)

			
			return Response(result,status=200,mimetype = "application/json")

		else:
			reason_status = "table not found"
			return jsonify({"status" : "error","reason" : reason_status})
	else:
		#user absent
		reason_status = "User not found"
		return jsonify({"status" : "error","reason" : reason_status})
	


@app.route('/api/table/index', methods = ['GET'])	
def api_table_index():

	'''
	Input:
		token
	
	Output:
		success : Returns details of all tables created by user with token :
					Name of the table
					table_id of the table
					URL where the data of the table is scraped
			
		error : user or table not found
	'''

	token = request.args['token']

	query_result = cursor.execute("select * from user where token = %s",(token,))
	if(query_result):
		cursor.execute("SELECT table_id, table_name, table_url FROM tables WHERE token = (%s)",(token,))
		#newList = list()
		data = cursor.fetchall()

		names = list(map(lambda x: x[0], cursor.description))	#names contains list of column names

		l = []
		row_count = 0
		for row in data:
			info = dict()
			for col in range(0,len(names)):
				info[names[col]]=row[col]
			
			l.append(info)
			row_count += 1
		
		return(jsonify(table_list = l))
	else:
		#user absent
		reason_status  ="User not found"
		return jsonify({"status" : "error","reason" : reason_status})


@app.route('/api/table/delete', methods = ['GET'])
def api_table_delete():
	'''
	Input:
		token
		table_id
	
	Output:
		success : table is deleted from Data database and corresponding entry removed from tables
		error : user or table not found
	'''

	token    = request.args['token']
	table_id = request.args['table_id']

	query_result = cursor.execute("select * from user where token = %s",(token,))

	if(query_result):
		try:
			client_cursor.execute("drop table "+ table_id)

			cursor.execute("delete from tables where table_id = %s",(table_id,))

			db.commit()	
			client_db.commit()
			global timer_dict
			print(timer_dict)
			timer_dict['table_id'].cancel()
			return jsonify({"status" : "success"})
			
		except:
			reason_status = "Table does not exist"
			return jsonify({"status" : "error","reason" : reason_status})

	else:
		reason_status = "User not found"
		return jsonify({"status" : "error","reason" : reason_status})



@app.route('/api/table/data.csv', methods = ['GET'])
def api_table_data_csv():
	'''
	Input:
		token
		table_id
	
	Output:
		success : CSV file containing all data in the table given by table_id
		error : user or table not found
	'''

	token    = request.args['token']
	table_id = request.args['table_id']
	
	#validate user
	
	query_result = cursor.execute("Select * from user where token = %s",(token,))
	if(query_result):
		
		#get data from the table desired by the user
		try:
			client_cursor.execute("select * from "+table_id)

			data = client_cursor.fetchall()


			# build the csv string
			ret_string = ""
			cursor.execute("select column_name from columns where table_id = %s" ,(table_id,))
			ret_list = list()
			for i in cursor.fetchall():
				ret_list.append(i[0])
			ret_string = ','.join(ret_list) + "\n"
			for row in data:
				ret_string = ret_string + ','.join(row) + '\n'
			
			resp = Response(ret_string, status=200, mimetype='application/force-download')
			return resp
		except:
			reason_status = "Table not found"
			return jsonify({"status" : "error","reason" : reason_status})
	else:
		reason_status =  "User not found"
		return jsonify({"status" : "error","reason" : reason_status})

		
def json2xml(json_obj, line_padding=""):
	'''
		Converts the input json string to XML format
	'''
	result_list = list()
	json_obj_type = type(json_obj)
	print(str(json_obj_type))
	if json_obj_type is list or json_obj_type is tuple:
		for sub_elem in json_obj:
			result_list.append(json2xml(sub_elem, line_padding))

		x = "\n</entry>\n<entry>\n".join(result_list)
		return "<entry>\n" + x + "\n</entry>"
	if json_obj_type is dict:
		for tag_name in json_obj:
			sub_obj = json_obj[tag_name]
			result_list.append("%s\t<%s>" % (line_padding, tag_name))
			result_list.append(json2xml(sub_obj, "\t\t" + line_padding))
			result_list.append("%s\t</%s>" % (line_padding, tag_name))

		return "\n".join(result_list)

	return "%s%s" % (line_padding, json_obj)



#working
@app.route('/api/table/data.xml', methods = ['GET'])
def api_table_data_xml():	
	'''
	Input:
		token
		table_id
	
	Output:
		success : XML file containing all data in the table given by table_id
		error : user or table not found
	'''

	token    = request.args['token']
	table_id = request.args['table_id']

	
	print("token is " + token)
	print("table_id is " + table_id)
	#validate user
	
	query_result = cursor.execute("Select * from user where token = %s",(token,))
	if(query_result):
		try:
			client_cursor.execute("select * from " + table_id)
			data = client_cursor.fetchall()

			names = list(map(lambda x: x[0], client_cursor.description)) #names contains list of column names

			l = []
			row_count = 0
			json_dump = ""
			for row in data:
				info = dict()
				for col in range(0,len(names)):
					info[names[col]]=row[col]
				
				l.append(info)
				row_count+=1
			
			data = str(l)
			data = data.replace('\'','"')
			#Json to xml parsing
			data = "<root>\n" + json2xml(json.loads(data)) + "</root>"
			
			resp = Response(data, status=200, mimetype='application/force-download')
			return resp
		except:
			reason_status = "Table not found"
			return jsonify({"status" : "error","reason" : reason_status})
	else:
		reason_status = "User not found"
		return jsonify({"status" : "error","reason" : reason_status})






@app.route('/api/table/data.json', methods = ['GET'])
def api_table_data_json():
	'''
	Input:
		token
		table_id
	
	Output:
		success : All data in the table given by table_id in JSON format
		error : user or table not found
	'''
	token    = request.args['token']
	table_id = request.args['table_id']
	
	#validate user
	
	query_result =  cursor.execute("Select * from user where token = %s",(token,))
	if(query_result):
		try:
			client_cursor.execute("select * from "+table_id)
			data = client_cursor.fetchall()


			names = list(map(lambda x: x[0], client_cursor.description)) #names contains list of column names

			l = []
			row_count = 0
			json_dump = ""
			for row in data:
				info = dict()
				for col in range(0,len(names)):
					info[names[col]]=row[col]
				
				l.append(info)
				row_count += 1

			# return jsonify(results = l)
			return Response(json.dumps(l), status=200, mimetype='application/force-download')
		except:
			reason_status = "Table not found"
			return jsonify({"status" : "error","reason" : reason_status})

	else:
		reason_status = "User not found"
		return jsonify({"status" : "error","reason" : reason_status})

def generate_class(table_id,list_of_columns):
		
		'''
		generates the content of the java file i.e. a class with attribute fields named by the columns names
		'''
		
		class_header = "public class " + table_id
		datatype = "public String"
		code = class_header + "\n" + "{\n"
		for i in list_of_columns:
			code += "\t" + datatype + " " + i + ";\n"
		code += "}"
		return code



@app.route('/api/table/getwrapper',methods = ['GET'])
def api_table_getwrapper():

	'''
	Input :
		token
		table_id

	Output : 
		.java file with the class
			name of class : table_id
			class attributes : column_names
	'''

	token    = request.args['token']
	table_id = request.args['table_id']
	print("cdsjbcn")
	query_result = cursor.execute("select * from user where token = %s",(token,))
	if(query_result):
		#generate the java file and return the file

		
		try:
			cursor.execute("select column_name from columns where table_id = %s",(table_id,))
			tuple_of_columns = cursor.fetchall()
			#after fetching the column names from the columns table
			cursor.execute("select table_name from tables where table_id = %s",(table_id,))
			table_name = cursor.fetchall()[0][0]
			#convert the tuple of tuples to a list -> for convenience
			list_of_columns = list()
			for i in tuple_of_columns:
				list_of_columns.append(i[0])

			#call the function to generate the java file
			response = make_response(generate_class(table_name,list_of_columns))
			response.headers["Content-Disposition"] = "attachment; filename=" + table_name + ".java"
			return response

		except:
			reason_status = "Table or column not found"
			return jsonify({"status" : "Failure","reason" : reason_status})
		
	else:
		#user absent
		reason_status = "User not found"
		return jsonify({"status" : "Failure","reason" : reason_status})




if __name__=='__main__':
	app.run()
