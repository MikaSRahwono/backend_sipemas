import requests
import os
import json

def sso_api(username, password):
    return requests.post('https://api.cs.ui.ac.id/authentication/ldap/v2/', data = {'username':username, 'password':password})

def get_faculty_info(kd_org):
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path, "faculty_info.json")

    with open(filename, "r") as fd:
        as_json = json.load(fd)
        if kd_org in as_json:
            return as_json[kd_org]

    return None