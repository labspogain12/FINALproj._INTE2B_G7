from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

print("Checking ENV variables:")
print("HOST:", os.getenv('DB_HOST'))
print("USER:", os.getenv('DB_USER'))
print("PASSWORD:", os.getenv('DB_PASSWORD'))
print("DATABASE:", os.getenv('DB_NAME'))
print("PORT:", os.getenv('DB_PORT'))

import mysql.connector

try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='blog_db',
        port=3306
    )
    if connection.is_connected():
        print("Connected to MySQL!")
        connection.close()
except mysql.connector.Error as e:
    print("Failed to connect:", e)

app = Flask(__name__) 

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME',),
    'port': int(os.getenv('DB_PORT', 3306))
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        print("MySQL connected.")
        return connection
    except mysql.connector.Error as e:
        print("Database connection failed:", e)
        return None

@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(posts)

@app.route('/api/posts/<int:id>', methods=['GET'])
def get_post(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    cursor.close()
    connection.close()
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post)

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.json
    required_fields = ['title', 'content', 'author']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO posts (title, content, author, tags) VALUES (%s, %s, %s, %s)",
        (data['title'], data['content'], data['author'], data.get('tags', ''))
    )
    connection.commit()
    post_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return jsonify({**data, 'id': post_id}), 201

@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    fields = []
    values = []
    for field in ['title', 'content', 'author', 'tags']:
        if field in data:
            fields.append(f"{field} = %s")
            values.append(data[field])

    if not fields:
        return jsonify({'error': 'No valid fields to update'}), 400

    fields.append("updated_at = CURRENT_TIMESTAMP")
    query = f"UPDATE posts SET {', '.join(fields)} WHERE id = %s"
    values.append(id)

    cursor = connection.cursor()
    cursor.execute(query, tuple(values))
    connection.commit()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Post not found'}), 404

    cursor.close()
    connection.close()
    return jsonify({'message': 'Post updated successfully'}), 200

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = connection.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    connection.commit()
    if cursor.rowcount == 0:
        return jsonify({'error': 'Post not found'}), 404
    cursor.close()
    connection.close()
    return jsonify({'message': 'Post deleted successfully'}), 200

if __name__ == '_main_': 
    app.run(debug=True)