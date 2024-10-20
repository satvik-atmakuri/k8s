from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your secret key')

POST_SERVICE_URL = os.environ.get('POST_SERVICE_URL', 'http://post-service:5000')

@app.route('/')
def index():
    try:
        response = requests.get(f'{POST_SERVICE_URL}/posts')
        response.raise_for_status()
        posts = response.json()
    except requests.RequestException as e:
        flash(f"Error fetching posts: {str(e)}", 'error')
        posts = []
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        new_post = {
            'title': request.form['title'],
            'content': request.form['content']
        }
        try:
            response = requests.post(f'{POST_SERVICE_URL}/posts', json=new_post)
            response.raise_for_status()
            flash('Post created successfully', 'success')
            return redirect(url_for('index'))
        except requests.RequestException as e:
            flash(f"Error creating post: {str(e)}", 'error')
    return render_template('create.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)