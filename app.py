from flask import Flask, request, render_template, url_for, send_from_directory
from werkzeug.utils import send_file
from route_functions import post_users
from teachable import get_courses
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html", styles=url_for('static', filename='index.css'))

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        (user_results, user_count) = post_users(request)
        return {"user_results": user_results, "user_count": user_count}
    else:
        return render_template("index.html", styles=url_for('static', filename='index.css'))

@app.route("/react", methods=['GET'])
def react():
    return send_from_directory("client", "public/index.html")

@app.route("/courses", methods=['POST'])
def courses():
    data = get_courses(request)
    return data