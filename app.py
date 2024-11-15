from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Konfiguracja bazy danych
db_config = {
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'mysql',  # W Docker Compose nazwa usługi to host
    'database': 'mydatabase',
}

@app.route('/helloworld', methods=['GET'])
def hello_world():
    return 'Hello World!'

@app.route('/add', methods=['POST'])
def add_data():
    data = request.json
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data_table (data) VALUES (%s)", (data['data'],))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/get', methods=['GET'])
def get_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data_table")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'data': rows})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
