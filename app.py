from flask import Flask, Response, request, jsonify, redirect, url_for, render_template,session, abort, send_from_directory
from flask_socketio import SocketIO, emit
from datetime import datetime
import pymongo
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
mongo = pymongo.MongoClient( os.environ['DB_PORT_27017_TCP_ADDR'],27017)
db = mongo['db1']
creds = db["creds"]
messages = db["messages"]
user = db["user"]

#sanity check 
@app.route("/ip")
def ip():
    return jsonify({'ip': request.environ['REMOTE_ADDR']})

#Static Files
@app.route('/src/<path:filename>')
def download_file(filename):
    print('----FILE REQUESTED: src/', filename)
    return send_from_directory('src/', filename)

# URL Routes
@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session['username']=='darsh':
        meds =  user.find_one({'username':'darsh'})['meds']
        return(render_template('index-p.html', username=session['username'], meds = meds))
    elif session['username']=='doctor':
        pt = user.find_one({'username':'darsh'})
        meds =  pt['meds']
        return(render_template('index-d.html', username=session['username'], meds = meds, pt=pt))

@app.route('/chat')
def chat():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return(render_template('chat.html'))

@app.route('/charts')
def chart():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return(render_template('charts.html'))

@app.route('/past')
def past():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        pt = user.find_one({'username':'darsh'})
        visits = pt['visits']
        return(render_template('visits.html',visit=visits,username=session['username']  ))

@app.route('/api/update', methods=['POST'])
def update():
    username = 'darsh'
    name = request.form['name']
    time = request.form['time']
   # reason = request.form['reason']
    old = user.find_one({'username':username})['meds']
    old.append({'name': name, 'time': time, })
    user.update_one({'username':username} ,{'$set' : {'meds': old}})
    return(redirect(url_for('index')))
@app.route('/api/alexa', methods=['GET'])
def alexa():
    username = 'darsh'
    meds = user.find_one({'username':username})['meds']
    return(jsonify(meds))

@app.route('/api/remove/<string:medname>', methods=['GET'])
def remove(medname):
    username = 'darsh'
    old = user.find_one({'username':username})['meds']
    old.remove(list(filter(lambda name: name['name'] == medname, old))[0])
    user.update_one({'username':username} ,{'$set' : {'meds': old}})
    return(redirect(url_for('index')))


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='GET':
        return redirect(url_for('index'))
    else:
        if user.count_documents({'username':str(request.form['username']), 'pin':str(request.form['password'])})==1:
            session['logged_in'] = True
            session['username'] = str(request.form['username'])
            return(redirect(url_for('index')))
        else:
            return(render_template('login.html', error=True))



@app.route('/logout')
def logout():
    session.clear()
    return(redirect(url_for('index')))

@app.route('/api/<string:username>/<string:time>')
def api_meds(username, time):
    global user
    meds = user.find_one({'username':username})
    
    return jsonify(meds['medtime'][time][0])

 # WebSocket Routes 
@socketio.on('connect', namespace='/test')
def test_connect():
    emit('cnct', {'msg': str( session['username']) })
    print('connected')
    emit('newcnct', {'msg': str( session['username']) },broadcast=True)
@socketio.on('emit_msg', namespace='/test')
def log_emit(message):
    emit('log_msg', {'msg':  str( session['username'])+': '+str(message)})
    print(message)

@socketio.on('broadcast_msg', namespace='/test')
def log_broadcast(message):
    emit('log_msg', {'msg':  str( session['username'])+': '+str(message)}, broadcast=True)
    print(message)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    emit('exit', {'msg': str( session['username']) }, broadcast=True)
    print('Client disconnected')





############# primitive BLOCKCHAIN ##########
import hashlib as hasher
import datetime
class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()
  
  def hash_block(self):
    sha = hasher.sha256()
    sha.update((str(self.index) + 
               str(self.timestamp) + 
               str(self.data) + 
               str(self.previous_hash)).encode())
    return sha.hexdigest()
def create_genisis_block():
    return Block(0,datetime.datetime.now(), "Genesis Block", "0")

def next_block(last_block, data):
  this_index = last_block.index + 1
  this_timestamp = datetime.datetime.now()
  this_data = data + str(this_index)
  this_hash = last_block.hash
  return Block(this_index, this_timestamp, this_data, this_hash)

def verify_blockchain(blockchain):
    for index in range(len(blockchain)):
        block = blockchain[index]
        if block.index==0:
            continue
        if(block.previous_hash != blockchain[index-1].hash):
            print("WARNING: Blockchain has been compromised at block {}".format(index-1))
    print("Blockchain Integrity Check Passed !")

blockchain = [ create_genisis_block() ]
previous_block = blockchain[0]

""" block_to_add = next_block(previous_block)
blockchain.append(block_to_add)
previous_block = block_to_add """



if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
