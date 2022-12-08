import json
import fake_useragent
import base64
import datetime as dt
import requests
from requests.structures import CaseInsensitiveDict

url = 'https://yougile.com/api-v2/'

def get_compans(log, pas):
    url_l = 'auth/companies'
    headers = CaseInsensitiveDict()
    data = {
        'login': log,
        'password': pas
    }
    headers['Content-Type'] = "application/json"
    user = fake_useragent.UserAgent().random
    headers['User-Agent'] = user
    response = requests.post((url + url_l), headers = headers,json = data)
    resp_dict = response.json()
    
    return resp_dict
def get_keys(log, pas, compId):
    url_l = 'auth/keys/get'
    headers = CaseInsensitiveDict()
    data = {
        'login': log,
        'password': pas,
         "companyId": compId
    }
    headers['Content-Type'] = "application/json"
    user = fake_useragent.UserAgent().random
    headers['User-Agent'] = user
    response = requests.post((url + url_l), headers = headers,json = data)
    resp_dict = response.json()
    
    return resp_dict

def create_key(log, pas, compId):
    url_l = 'auth/keys'
    headers = CaseInsensitiveDict()
    data = {
        'login': log,
        'password': pas,
         "companyId": compId
    }
    headers['Content-Type'] = "application/json"
    user = fake_useragent.UserAgent().random
    headers['User-Agent'] = user
    response = requests.post((url + url_l), headers = headers,json = data)
    resp_dict = response.json()
    
    return resp_dict

def del_key (key):
    url_l = 'auth/keys/' + key
    headers = CaseInsensitiveDict()
    headers['Content-Type'] = "application/json"
    user = fake_useragent.UserAgent().random
    headers['User-Agent'] = user
    response = requests.post((url + url_l), headers = headers)
    resp_dict = response.json()
    
    return resp_dict

def get_workers(key):
    url_l = 'users'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + key,
        'User-Agent' : fake_useragent.UserAgent().random
    }
    response = requests.post((url + url_l), headers = headers)
    resp_dict = response.json()
    
    return resp_dict
    
def get_proj(key):
    url_l = 'projects'
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["includeDeleted"] = "True"
    response = requests.get((url + url_l), headers = headers)
    resp_dict = response.json()
    
    return resp_dict