from flask.wrappers import Request
from typing import List, Tuple, TypedDict, Union, Literal
import csv
from teachable import create_user, add_user_to_course
from helpers import file_is_valid

class UserResult(TypedDict):
    id_: Union[str, int, None]
    details: str
    status: Literal["already in course", "success", "ERROR - not added", "ERROR - not created", "ERROR - file not valid"]
    status_code: Union[int, None]

def post_users(request: Request) -> Tuple[list[UserResult], int]:        
    username = request.form['username']
    course_id = request.form['course_id']
    password = request.form['password']
    csv_data = request.files['new_user_file']
    
    user_count = 0
    user_results: List[UserResult] = []

    # Check for CSV file
    if file_is_valid(csv_data):
        file_path = f"uploads/{csv_data.filename}"
        csv_data.save(file_path)

        # Read the CSV file
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)

            # Loop through the rows
            for row in csv_reader:
                new_user_first_name = row[0]
                new_user_last_name = row[1]
                new_user_email = row[2]
                # Create a summary of the user
                full_user_details = new_user_first_name + " " + new_user_last_name + " " + new_user_email
                
                # Create the user via POST request to the API
                created = create_user(admin_username=username, admin_password=password, name=f"{new_user_first_name}{new_user_last_name}", email=new_user_email)
                
                if created.ok:
                    # User created successfully
                    new_user_id = created.json()['id']
                    # Add the user to the course via PUT request to the API
                    added = add_user_to_course(course_id=course_id, user_id=new_user_id, username=username, password=password)
                    if added.ok == 200: # User added to course successfully
                        user_count += 1
                        user_results.append({"id_": new_user_id, "details": full_user_details, "status": "success", "status_code": added.status_code})
                    elif added.status_code == 422: # User already in course
                        user_results.append({"id_": new_user_id, "details": full_user_details, "status": "already in course", "status_code": added.status_code})
                    else: # User not added to course
                        user_results.append({"id_": new_user_id, "details": full_user_details, "status": "ERROR - not added", "status_code": added.status_code})
                else: # User not created
                    user_results.append({"id_": 0, "details": full_user_details, "status": "ERROR - not created", "status_code": created.status_code})
    else:
        user_results.append({"id_": 0, "details": "ERROR - file not valid", "status": "ERROR - file not valid", "status_code": None})
    return (user_results, user_count)


