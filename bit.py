from fast_bitrix24 import *
from datetime import datetime as dt, timedelta, timezone
f = open('credentials_b.txt','r')

webhook = f.read()
f.close()
b = Bitrix(webhook[:-1])

#Получить список всех проектов со всеми задачами(карточками)
def get_list_project():
    tasks = b.get_all('tasks.task.list')
    desks = {}
    for task in tasks:
        if len(task['group']) != 0:
            if not desks.get(task['group']['name'], False) or len(desks) == 0:
                desks[task['group']['name']] = {}
            desks[task['group']['name']][len(desks[task['group']['name']])]= task
    return desks

#Метод для получения списка комментариев по задаче
def get_list_of_comm(id_task):
    param = {'TASKID': id_task}
    list_comm = b.get_all('task.commentitem.getlist',param)
    return list_comm


#Получить список стадий в проекте(stage_id)
def get_list_of_stage(id_group):
    param = {'entityId': id_group,
              'isAdmin':True }
    list_stage = b.get_all('task.stages.get',param)
    return list_stage

# resolving stageId in stage_title
def resovle_stage(id_group,stageId):    
    list_stage = get_list_of_stage(id_group)
    if len(list_stage) > 0:
        title = list_stage[str(stageId)]['TITLE']
    
        return title
    else:
        return 'none'

#Добавить колонку в проект
def add_stage_of_group(id_group,title):
    param = {  "fields":{ 'TITLE': title,
               'ENTITY_ID': id_group,
               'isAdmin' : True
               }
            }
    result = b.call('task.stages.add',param)
    return result

#Удалить колонку в проекте
def del_stage_of_group(id_stage):
    param = {  
        'id' : id_stage,
        'isAdmin' : True
            }
    result = b.call('task.stages.delete',param)
    return result

#Изменить колонку в проекте
def upd_stage_of_group(id_stage,title):
    param = {  "id" : id_stage,
                "fields":{ 'TITLE': title,
               'isAdmin' : True
               }
            }
    result = b.call('task.stages.update',param)
    return result    

#Карточки
#Добавить карточку в проект
def add_task_of_group(id_group,title,descripton,id_stage, created_by, id_responsible):
    param = {  "fields":{ 
                'TITLE': title,
               'DESCRIPTION': descripton,
               'GROUP_ID' : id_group,
               'STAGE_ID' : id_stage,
               'CREATED_BY' : created_by,
               'RESPONSIBLE_ID' : id_responsible
               }
            }
    result = b.call('tasks.task.add',param)
    return result

#Удалить карточку из проекта
def del_task_of_group(task_id):
    param = {  
        'taskId': task_id
            }
    result = b.call('tasks.task.delete',param)
    return result

#Изменить карточку в проекте
def upd_task_of_group(id_task,title,descripton,id_stage):
    param = {  
        'taskId' : id_task,
        "fields":{ 
                'TITLE': title,
               'DESCRIPTION': descripton,
               'STAGE_ID' : id_stage
               }
            }
    result = b.call('tasks.task.update', param)
    return result

def get_curr_state_bit():
    infa = []
    proj_avec_tasks = get_list_project()
    proj_keys = list(proj_avec_tasks.keys())
    for i in range (len(proj_keys)):
        infa.append([])
        infa[i].append(proj_keys[i])
        curr_tasks = list(proj_avec_tasks[proj_keys[i]].keys())
        infa[i].append([])        
        for j in range(len(curr_tasks)):
            infa[i][1].append([])
            infa[i][1][j].append(proj_avec_tasks[proj_keys[i]][curr_tasks[j]]['id'])
            infa[i][1][j].append(proj_avec_tasks[proj_keys[i]][curr_tasks[j]]['title'])
            infa[i][1][j].append(proj_avec_tasks[proj_keys[i]][curr_tasks[j]]['description'])
            if (type(proj_avec_tasks[proj_keys[i]][curr_tasks[j]]['deadline']) == str ):
                dat = proj_avec_tasks[proj_keys[i]][curr_tasks[j]]['deadline'].replace('T',' ')
                infa[i][1][j].append(dt.strptime(dat[:-6]+' '+ dat[-6:], "%Y-%m-%d %H:%M:%S %z"))
            else :
                infa[i][1][j].append('')
            infa[i][1][j].append(proj_avec_tasks[proj_keys[i]][curr_tasks[j]]['status'])
            infa[i][1][j].append(
                resovle_stage(
                    proj_avec_tasks[proj_keys[i]][curr_tasks[j]]['groupId'],
                    proj_avec_tasks[proj_keys[i]][curr_tasks[j]]['stageId']
                    )
                )
        infa[i].append(proj_avec_tasks[proj_keys[i]][curr_tasks[0]]['groupId'])
    return infa

if __name__ == '__main__':
    # res = get_list_project()
    # alm = list(res.keys())
    # print(alm)
    # print(list(res[alm[0]].keys()))
    pass
    #upd_stage_of_group(10,"В процессе выполнения")
    #add_task_of_group(2,'Работа в понедельник в 13','Сейчас 13:48',10, 1, 1)
    #res = get_list_project()
    #print(res)
    #del_task_of_group(10)
    #print(get_list_of_stage(2))
    #add_stage_of_group(2,"В завершении+")
    #stage = get_list_of_stage(2)
    #print(stage)
    #upd_task_of_group(12,"Работа в понедельник в 14","Сейчас 13;57",36)
    #del_stage_of_group(8)
    # print(get_list_of_stage(2))

    