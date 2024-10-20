from flask import Flask, request, jsonify, abort
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres-service'),
        database=os.environ.get('DB_NAME', 'posts_db'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'password')
    )

@app.route('/posts', methods=['GET', 'POST'])
def handle_posts():
    print(f"Received {request.method} request to /posts")
    if request.method == 'GET':
        print("Handling GET request")
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute('SELECT * FROM posts')
                    posts = cur.fetchall()
            return jsonify(posts)
        except Exception as e:
            print(f"Error in GET /posts: {str(e)}")
            return jsonify({"error": str(e)}), 500

    if request.method == 'POST':
        print("Handling POST request")
        try:
            new_post = request.json
            title = new_post.get('title')
            content = new_post.get('content')

            if not title:
                abort(400, "Title is required")

            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING id', (title, content))
                    new_id = cur.fetchone()[0]
                    conn.commit()

            new_post['id'] = new_id
            return jsonify(new_post), 201
        except Exception as e:
            print(f"Error in POST /posts: {str(e)}")
            return jsonify({"error": str(e)}), 500

@app.route('/dbtest')
def db_test():
    print("Received request to /dbtest")
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
                result = cur.fetchone()
        return jsonify({"status": "Database connection successful", "result": result})
    except Exception as e:
        print(f"Error in /dbtest: {str(e)}")
        return jsonify({"status": "Database connection failed", "error": str(e)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"An unhandled error occurred: {str(e)}")
    return jsonify(error=str(e)), 500

@app.route('/')
def hello():
    return "Hello from Post Service!"

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000)
