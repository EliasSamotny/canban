import json
import fake_useragent
import datetime as dt
import requests
from requests.structures import CaseInsensitiveDict

url = 'https://yougile.com/api-v2/'

def get_compans(log, pas): # get companies by log et pass
    url_l = 'auth/companies'
    headers = CaseInsensitiveDict()
    data = {
        'login': log,
        'password': pas
    }
    headers['Content-Type'] = "application/json"
    headers['User-Agent'] = fake_useragent.UserAgent().random
    response = requests.post((url + url_l), headers = headers,json = data)
    
    return response
def get_keys(log, pas, compId): # get key pour company
    url_l = 'auth/keys/get'
    headers = CaseInsensitiveDict()
    data = {
        'login': log,
        'password': pas,
         "companyId": compId
    }
    headers['Content-Type'] = "application/json"
    headers['User-Agent'] = fake_useragent.UserAgent().random
    response = requests.post((url + url_l), headers = headers,json = data)
    
    return response

def create_key(log, pas, compId): # create a key pour company
    url_l = 'auth/keys'
    headers = CaseInsensitiveDict()
    data = {
        'login': log,
        'password': pas,
        "companyId": compId
    }
    headers['Content-Type'] = "application/json"
    headers['User-Agent'] = fake_useragent.UserAgent().random
    response = requests.post((url + url_l), headers = headers,json = data)
    return response

def del_key (key): # delete a key of company
    url_l = 'auth/keys/' + key
    headers = CaseInsensitiveDict()
    headers['Content-Type'] = "application/json"
    headers['User-Agent'] = fake_useragent.UserAgent().random
    response = requests.post((url + url_l), headers = headers)
    
    return response

def get_workers(key): # get list of workers of comp
    url_l = 'users'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + key,
        'User-Agent' : fake_useragent.UserAgent().random
    }
    response = requests.post((url + url_l), headers = headers)
    return response
    
def get_proj(key): # get projects by key
    url_l = 'projects'
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["includeDeleted"] = "False"
    headers['User-Agent'] = fake_useragent.UserAgent().random
    response = requests.get((url + url_l), headers = headers)
    
    return response

def get_board(key, projId):
    
    url_l = "boards"
    headers = CaseInsensitiveDict()
    querystring = {"projectId":projId}
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["includeDeleted"] = "False"
    headers['User-Agent'] = fake_useragent.UserAgent().random
    response = requests.get((url + url_l), headers = headers, params=querystring)
    
    return response

def get_cols(key,board_id):
    
    url_l = "columns"
    headers = CaseInsensitiveDict()
    querystring = {"boardId": board_id}
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["includeDeleted"] = "False"
    headers['User-Agent'] = fake_useragent.UserAgent().random
    response = requests.get((url + url_l), headers = headers, params=querystring)
    
    return response

def get_tasks(key, col_id):
    
    url_l = "tasks"
    headers = CaseInsensitiveDict()
    querystring = {"columnId": col_id}
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["includeDeleted"] = "False"
    headers['User-Agent'] = fake_useragent.UserAgent().random
    response = requests.get((url + url_l), headers = headers, params=querystring)
    
    return response

def get_users_in_task(key, us_ids):
    if type(us_ids) is str:
        url_l = "users/" + us_ids
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = "Bearer " + key
        headers['User-Agent'] = fake_useragent.UserAgent().random
        response = requests.get((url + url_l), headers = headers)
        if response.status_code == 200:
            response = response.json()
            return response['realName']
    else:
        infa = []
        for i in range(len(us_ids)):
            url_l = "users/" + us_ids[i]
            headers = CaseInsensitiveDict()
            headers["Content-Type"] = "application/json"
            headers["Authorization"] = "Bearer " + key
            headers['User-Agent'] = fake_useragent.UserAgent().random
            response = requests.get((url + url_l), headers = headers)
            if response.status_code == 200:
                response = response.json()
                print(response)
                infa.append(response['realName'])
        return infa
    