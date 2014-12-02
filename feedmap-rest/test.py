from datetime import timedelta  
from flask import Flask, make_response, request, current_app,json
from functools import update_wrapper
import MySQLdb
import sys
app = Flask(__name__)
connection=MySQLdb.connect(host = "127.0.0.1", user = "root", passwd = "root", db = "TEST")
cursor = connection.cursor ()

@app.route('/getfeed')
@crossdomain(origin='*')
def getFeed():
   
    cursor.execute ("select * from FeedsTest")
    data = cursor.fetchall()
    
    json ='{"twitterId":"","lng": "24.8600","lat": "67.0100","tweetCount": "4","handle": "feedmap","favorites": "4", "retweets": "5","tweet":"firsttweet","refute":"","approve":"","city":""}'
    
    #for row in data:
        #thing =row[0]+thing
#Response(json.dumps(mydata),  mimetype='application/json')
    return Respponse(json,mimetype='application/json')

@app.route('/citytweets',methods=['GET'])
def getTweetsByCity():
    city = request.args.get('city')
    query = 'Select * from FeedsTest Where City like (%s)'
    cursor.execute(query,[city])
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    result = []
    for row in rows:
        row = dict(zip(columns, row))
        result.append(row)   
    print result
    
    return data


def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):  
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator



if __name__ == '__main__':
    app.run(host='0.0.0.0')