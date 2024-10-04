from flask import Flask, request, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'GRAPHITE/c60',  # Replace with your password
    'database': 'test'
}

@app.route('/')
def index():
    return render_template('index.html')  # Render the chat interface

@app.route('/send', methods=['POST'])
def send():
    con = None  # Initialize con outside of the try block
    try:
        con = mysql.connector.connect(**db_config)
        cursor_obj = con.cursor()

        username = request.form.get('username')
        message = request.form.get('message')

        # Insert the message into the database
        cursor_obj.execute("INSERT INTO messages (username, message) VALUES (%s, %s)", (username, message))
        con.commit()

        return jsonify(success=True)

    except mysql.connector.Error as err:
        return jsonify(success=False, error=str(err))

    finally:
        if con and con.is_connected():  # Check if con was successfully initialized
            cursor_obj.close()
            con.close()

@app.route('/messages', methods=['GET'])
def messages():
    con = None  # Initialize con outside of the try block
    try:
        con = mysql.connector.connect(**db_config)
        cursor_obj = con.cursor()
        
        cursor_obj.execute("SELECT username, message, timestamp FROM messages ORDER BY timestamp DESC")
        rows = cursor_obj.fetchall()
        
        return jsonify(messages=[{'username': row[0], 'message': row[1], 'timestamp': row[2].strftime('%Y-%m-%d %H:%M:%S')} for row in rows])

    except mysql.connector.Error as err:
        return jsonify(success=False, error=str(err))

    finally:
        if con and con.is_connected():  # Check if con was successfully initialized
            cursor_obj.close()
            con.close()

if __name__ == '__main__':
    app.run(debug=True)