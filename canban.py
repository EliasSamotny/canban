import json
import fake_useragent
from datetime import datetime as dt, timedelta, timezone
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
            return [response['realName']]
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

def get_curr_state_canban(key):
    req_proj = get_proj(key)
    proj = []
    if req_proj.status_code != 200:
        print ('Erreur ' + str(req_proj.status_code) + '. Something wrong with a key.')
    else:
        req_proj = req_proj.json()        
        kol_proj = int(req_proj['paging']["count"])
        for l in range(kol_proj):          
            proj.append([])
            proj[l].append(req_proj['content'][l]['id']) 
            proj[l].append(req_proj['content'][l]['title'])    
            
            req_board = get_board(key, proj[l][0])
            req_board_json = req_board.json()
            if req_board.status_code == 200 and int(req_board_json['paging']["count"]) > 0:
                proj[l].append([req_board_json['content'][0]['id'],[]]) # the board

                req_columns = get_cols(key,proj[l][2][0])
                req_columns_json = req_columns.json()
                if req_columns.status_code == 200 and int(req_columns_json['paging']["count"]) > 0:
                    for i in range(int(req_columns_json['paging']["count"])):
                        proj[l][2][1].append([req_columns_json['content'][i]['id'],
                                    req_columns_json['content'][i]['title'],
                                    []]) # the board
                        
                        req_tasks = get_tasks(key, proj[l][2][1][i][0])
                        req_tasks_json = req_tasks.json()
                        if req_tasks.status_code == 200:
                            for j in range(int(req_tasks_json['paging']["count"])):
                                cont = [
                                    req_tasks_json['content'][j]['id'],
                                    req_tasks_json['content'][j]['title'],                     
                                ]
                                if 'description' in req_tasks_json['content'][j]:
                                    cont.append(req_tasks_json['content'][j]['description'])
                                else: cont.append('')
                                if 'deadline' in req_tasks_json['content'][j] and 'deadline' in req_tasks_json['content'][j]['deadline']:
                                    cont.append(dt.fromtimestamp(req_tasks_json['content'][j]['deadline']['deadline']//1000, tz=timezone(timedelta(hours = 3))))
                                else:
                                    cont.append('')
                                if 'completed' in req_tasks_json['content'][j]:    
                                    cont.append(req_tasks_json['content'][j]['completed'])
                                else: cont.append('')
                                if 'assigned' in req_tasks_json['content'][j]:
                                    cont.append(get_users_in_task(key, req_tasks_json['content'][j]['assigned']))
                                else: cont.append([])
                                proj[l][2][1][i][2].append(cont)
                        else: print ("Task \""+ proj[l][2][j][1] + '\" with id \"'+ proj[l][2][j][0] + "\" n\'existe pas!")
            
            # elif int(req_board_json['paging']["count"]) == 0:
            #     print ('No boards in project \"' + proj[l][1] + "\"")  
            # else: print ("Something wrong about boards")
        
        # print ('Canban content:')
        for i in range(len(proj)): # projects
            
            # print(' id in canban = '+ proj[i][0])            
            # print(' title of project = '+ proj[i][1])
            # print(' id of board = ' + proj[i][2][0])
            # print(' meta: num of cols = ' + str(len(proj[i][2][1])))
            for j in range(len(proj[i][2][1])): # columns
                # print ('  id of col = ' + proj[i][2][1][j][0])
                
                # print ('  title of col = ' + proj[i][2][1][j][1])
                for k in range(len(proj[i][2][1][j][2])): #cards
                    # print('    id of card = ' + proj[i][2][1][j][2][k][0])                    
                    # print('    title of card = ' + proj[i][2][1][j][2][k][1])
                    # print('    decription of card = ' + proj[i][2][1][j][2][k][2])
                    # print('    deadline of card = ' + str(proj[i][2][1][j][2][k][3]))
                    # print('    Is complete? = ' + str(proj[i][2][1][j][2][k][4]))
                    # print('    Assigned users = ' + str(proj[i][2][1][j][2][k][5]))
                    del proj[i][2][1][j][2][k][0] #id card
                del proj[i][2][1][j][0] # id col
            del proj[i][0]# id proj
            del proj[i][1][0] # id board
                
    return proj

def get_list_of_cols(key):
    canban = get_curr_state_canban(key)
    list_cols = []
    # print (canban)
    for i in range(len(canban)):        
        cols = []
        for j in range(len(canban[i][1][0])):
            cols.append(canban[i][1][0][j][0])
        list_cols.append([canban[i][0],cols])
    return list_cols

def from_cols_to_tasks(projs):
    nouv_list = []
    for i in range(len(projs)):
        nouv_list.append([])
        nouv_list[i].append(projs[i][0])
        nouv_list[i].append([])
        cols = projs[i][1][0]
        for j in range(len(cols)):
            tasks = cols[j][1]
            for k in range(len(tasks)):                
                nouv_list[i][1].append(
                    [tasks[k][0],
                     tasks[k][1],
                     tasks[k][2],
                     tasks[k][3],
                     cols[j][0]
                                        ])    
    return nouv_list
