from canban import create_key, get_board, get_cols, get_compans,get_keys,get_proj, get_tasks, get_users_in_task

log = 'ilya.madaev2002e@gmail.com'
pas = 'jEsuisFragile_1'

comp = get_compans(log,pas).json()['content'][0]['id']

key_req = get_keys(log,pas,comp)
if key_req.status_code == 200:
    key = key_req.json()[0]['key']
else:
    key = create_key(log, pas, comp).json()["key"]

print (key)
req_proj = get_proj(key)

if req_proj.status_code == 200:
    req_proj = req_proj.json()
    proj = []
    proj.append(req_proj['content'][0]['id']) 
    proj.append(req_proj['content'][0]['title'])    
    
    req_board = get_board(key, proj[0])
    req_board_json = req_board.json()
    if req_board.status_code == 200 and int(req_board_json['paging']["count"]) > 0:
        proj.append([req_board_json['content'][0]['id'],[]]) # the board

        req_columns = get_cols(key,proj[2][0])
        req_columns_json = req_columns.json()
        if req_columns.status_code == 200 and int(req_columns_json['paging']["count"]) > 0:
            for i in range(int(req_columns_json['paging']["count"])):
                proj[2][1].append([req_columns_json['content'][i]['id'],
                            req_columns_json['content'][i]['title'],
                            []]) # the board
                
                req_tasks = get_tasks(key, proj[2][1][i][0])
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
                        if 'completed' in req_tasks_json['content'][j]:    
                            cont.append(req_tasks_json['content'][j]['completed'])
                        else: cont.append('')
                        print (req_tasks_json['content'][j])
                        cont.append(get_users_in_task(key, req_tasks_json['content'][j]['assigned']))
                        
                        proj[2][1][i][2].append(cont)
                else: print ("Task \""+ proj[2][j][1] + '\" with id \"'+ proj[2][j][0] + "\" n\'existe pas!")
    
    elif int(req_board_json['paging']["count"]) > 0:
        print ('No boards in project \"' + proj[1] + "\"")  
    else: print ("Something wrong about boards")
    
    print (proj)    
else: print ('No information about project.')

