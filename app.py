from flask import Flask, request, render_template, url_for
from teachable import add_user_to_course, create_user

import csv

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html", styles=url_for('static', filename='index.css'))

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        username = request.form['username']
        course_id = request.form['course_id']
        password = request.form['password']

        csv_data = request.files['new_user_file']
        user_count = 0
        message = ""
        if csv_data.filename != '':
            file_path = f"uploads/{csv_data.filename}"
            csv_data.save(file_path)
            
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                for row in csv_reader:
                    new_user_first_name = row[0]
                    new_user_last_name = row[1]
                    new_user_email = row[2]
                    full_user_details = new_user_first_name + " " + new_user_last_name + " " + new_user_email
                    created = create_user(admin_username=username, admin_password=password, name=f"{new_user_first_name}{new_user_last_name}", email=new_user_email)
                    print(created.status_code)
                    if created.ok:
                        new_user_id = created.json()['id']
                        added = add_user_to_course(course_id=course_id, user_id=new_user_id, username=username, password=password)
                        print(added.status_code)
                        if added.ok == 200:
                            user_count += 1
                            message = f"{user_count} users added to {added.json()['name']} course."
                        elif added.status_code == 422:
                            message += f"{full_user_details} already exists in the course.\n"
                        else:
                            message += f"Failed to add {full_user_details}."
                    else:
                        message += f"failed to create {full_user_details}."

        return render_template("confirm.html", message=message, styles=url_for('static', filename='index.css'))
    else:
        return render_template("users.html", styles=url_for('static', filename='index.css'))
