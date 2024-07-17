from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)
DATABASE = 'battery_status.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS battery_status (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ip TEXT,
                        mac TEXT,
                        port TEXT,
                        status INTEGER,
                        battery_level INTEGER,
                        voltage INTEGER,
                        current INTEGER,
                        cell1 INTEGER,
                        cell2 INTEGER,
                        cell3 INTEGER,
                        cell4 INTEGER,
                        cell5 INTEGER,
                        cell6 INTEGER,
                        cell7 INTEGER,
                        cell_temperature INTEGER,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()
    conn.close()

@app.route('/api/upload.api', methods=['POST'])
def upload_data():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO battery_status (ip, mac, port, status, battery_level, voltage, current, cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell_temperature) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (data['IP'], data['MAC'], data['UsbPortLocation'], data['Status'], data['BatteryLevel'], data['Voltage'], data['Current'],
                    data['Cell1'], data['Cell2'], data['Cell3'], data['Cell4'], data['Cell5'], data['Cell6'], data['Cell7'], data['CellTemper']))
    conn.commit()
    conn.close()
    socketio.emit('update', data, broadcast=True)
    return jsonify({
        "Result": "__OK__",
        "ResultCode": "100",
        "ResultDesc": "success",
        "ResponseDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S %f")
    })

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM battery_status ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return render_template('index.html', rows=rows)

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=8080)
