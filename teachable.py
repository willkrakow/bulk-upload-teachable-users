from typing import Literal, TypedDict, Union
import requests
import base64

TEACHABLE_URL_BASE = 'https://learn.plantpurecommunities.org/api/v1'

class NewUser(TypedDict):
    created_at: str
    current_sign_in_at: str
    sign_in_count: int
    role: Literal['student', 'owner', 'affiliate']
    sanitized_name: str
    id: int


def create_session(username, password):
    """
    Creates a session for the given username and password.
    """
    encode_basic_auth = base64.b64encode(bytes(f"{username}:{password}", 'utf-8')).decode('utf-8')
    teachable_session = requests.Session()
    teachable_session.auth = (username, password)
    teachable_session.headers['Content-Type'] = 'application/json;charset=UTF-8'
    teachable_session.headers['Accept'] = 'application/json'
    teachable_session.headers['Authorization'] = f"Basic {encode_basic_auth}"
    return teachable_session

def add_user_to_course(course_id: Union[int, str], user_id: int, username: str, password: str):
    """
    Add users to a course
    """
    url = f"{TEACHABLE_URL_BASE}/users/{user_id}/enrollments"
    data = {
        "course_id": course_id,
    }
    teachable_session = create_session(username, password)
    response = teachable_session.post(url, json=data)
    return response

def create_user(email: str, name: str, admin_username: str, admin_password: str) -> requests.Response:
    url = f"{TEACHABLE_URL_BASE}/users"
    data = {
        "email": email,
        "name": name,
    }
    teachable_session = create_session(admin_username, admin_password)
    response = teachable_session.post(url, json=data)
    return response

def get_users(username: str, password: str) -> requests.Response:
    url = f"{TEACHABLE_URL_BASE}/users"
    teachable_session = create_session(username, password)
    response = teachable_session.get(url)
    return response
