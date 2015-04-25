
from flask import Flask, jsonify
from flask import request
import MySQLdb
import httplib2
from httplib2 import Http
from urllib import urlencode

#get username password from a config file 
auth = open('config','r')
d1 = auth.readlines()

u1 = d1[1].split(":")[1].strip()
p1 = d1[2].split(":")[1].strip()


#host at which database resides
hostname="192.168.56.1"

password = p1
username = u1

dbname="Excavator"

print("username : "+u1)
print("password : .*")

app = Flask(__name__)


db = MySQLdb.connect(host=hostname,user=username,passwd=password,db=dbname)
cursor = db.cursor()
client_db=MySQLdb.connect(host="192.168.56.1",user="root",passwd="", db="Excavator")
client_cursor=client_db.cursor()

#this method fetches all the rows in the table
@app.route("/getAll")
def getAll():
    db = MySQLdb.connect(host=hostname,user=username,passwd=password,db=dbname)
    cur = db.cursor()
    token    = request.args['token']
    #table_id = request.args['table_id']

    query_result = cursor.execute("select * from user where token = %s",(token,))
    #get table name
    APIkey = request.args.get('APIkey','no')
    tablename= APIkey
    if(query_result):
        try:
            if(request.args.get("limit","no")!="-1"):
                res=cur.execute("select * from %s limit %s"%(tablename,request.args.get('limit','no'))) 
            else:
                res=cur.execute("select * from %s"%(tablename,))


            res1=cur.fetchall()
            
            # this is used to get the column names in the table
            names = list(map(lambda x: x[0], cur.description))
            l=[]
            row_count=0
            json_dump=""
            for row in res1:
                info=dict()
                for col in range(0,len(names)):
                    info[names[col]]=row[col]
                l.append(info)
                row_count+=1

            p=[]
            if request.args.get('filterCount','no') != 'no':
                for i in range(0,int(request.args.get('filterCount','no'))):
                    p.append([request.args.get("filteratt"+str(i)),request.args.get("filterop"+str(i)),request.args.get("filterkey"+str(i))] )  
                
                l=filters(l,int(request.args.get('filterCount','no')),p)
            
            #jasonify method converts to json 
            return jsonify(results=l)
        except:
            return(jsonify({'status':'failure','reason':'table does not exist'}))
    else :
        return jsonify({'status':'failure','reason':'user does not exist'})

#this method fetches 'n' rows from the table. limit has to be passed in the URL
@app.route("/getLastN")
def getLastN():
    
    db = MySQLdb.connect(host=hostname,user=username,passwd=password,db=dbname)
    cur = db.cursor()
    token    = request.args['token']
    #get table name
    APIkey = request.args.get('APIkey','no')
    ln = request.args.get('getLastN','no')
    tablename=APIkey

    query_result = cursor.execute("select * from user where token = %s",(token,))
    if(query_result):
        try:
            sql="select * from %s"%(tablename,)
            res=cur.execute(sql)
            res1=cur.fetchall()
            names = list(map(lambda x: x[0], cur.description))
            l=[]
            row_count=0
            json_dump=""
            for row in res1:
                info=dict()
                for col in range(0,len(names)):
                    info[names[col]]=row[col]
                l.append(info)
                row_count+=1
            l=l[::-1]
            if request.args.get('getLastN','no')!= 'no':
                l=l[:int(ln)]
            #getLastN N
            p=[]

            if request.args.get('filterCount','no') != 'no':
                for i in range(0,int(request.args.get('filterCount','no'))):
                    p.append([request.args.get("filteratt"+str(i)),request.args.get("filterop"+str(i)),request.args.get("filterkey"+str(i))] )  
                
                l=filters(l,int(request.args.get('filterCount','no')),p)
            
            #return first n (limit)
            if(request.args.get("limit","no")!="-1"):
                return jsonify(results=l[:int(request.args.get("limit",""))])
            else:
                return jsonify(results=l)
        except:
                return jsonify({'status':'failure','reason':'invalid table name'})
    else:
        return jsonify({'status':'failure','reason':'user does not exist'})


# this method fetches the rows as specified by the user through the 'execute' parameter in the URL
@app.route("/execute")
def execute():
    db = MySQLdb.connect(host=hostname,user=username,passwd=password,db=dbname)
    cur = db.cursor()
    
    
    tablename= ""
    
    cmd=request.args.get('execute','no')    

    #check table name is same as table name obtained from API KEY
    #if not same return permission denied
    try:
        if True :

            res=cur.execute(cmd) 
            res1=cur.fetchall()
            l=[]
            names = list(map(lambda x: x[0], cur.description))
            row_count=0
            json_dump=""
            for row in res1:
                info=dict()
                for col in range(0,len(names)):
                    info[names[col]]=row[col]
                l.append(info)
                row_count+=1
            #return first n (limit)
            
            if request.args.get('filterCount','no') != 'no':
                for i in range(0,int(request.args.get('filterCount','no'))):
                    p.append([request.args.get("filteratt"+str(i)),request.args.get("filterop"+str(i)),request.args.get("filterkey"+str(i))] )  
            
                l=filters(l,int(request.args.get('filterCount','no')),p)
            if(request.args.get("limit","no")!="-1"):
                return jsonify(results=l[:int(request.args.get("limit",""))])
            else:
                return jsonify(results=l)
        else:
            return "permission denied"
    except:
        #extract proper error code
        return jsonify({'status':'failure','reason':'undertermined'})

def filters(l,num_attr,params):
    after_filter=l
    for i in range(0,num_attr):
        if(int(params[i][1])==2):
            after_filter=MyFilter(lambda x: int(x[params[i][0]])<int(params[i][2]),after_filter) 
        elif(int(params[i][1])==1):
            after_filter=MyFilter(lambda x: int(x[params[i][0]])>int(params[i][2]),after_filter) 
        elif(int(params[i][1])==0):
            after_filter=MyFilter(lambda x: int(x[params[i][0]])==int(params[i][2]),after_filter) 
    return after_filter


def MyFilter(fun,l):
    temp=[]
    for i in l:
        if fun(i):
            temp.append(i)
    return temp
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug="true",port=5001)
