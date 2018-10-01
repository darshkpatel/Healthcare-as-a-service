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
    else:
        return(render_template('index.html'))
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return(render_template('admin/index.html'))
        
@app.route('/chat')
def chat():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return(render_template('chat.html'))

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
    meds['medtime'][time]
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

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
