from bit import get_curr_state_bit, get_list_of_stage
from canban import create_key, from_cols_to_tasks,  get_compans, get_curr_state_canban,get_keys, get_list_of_cols

def index_delement_in_bit(sett,el):
    for i in range(len(sett)):
        if sett[i][0] == el:
            return i
    return -1

def if_all_corresp(you, bit):
    for i in range(len(you)):
        for j in range(len(bit[i][2])):
            if (not bit[i][2][j][1] in you[i][1]):
                return False
        
    return True
if __name__ == '__main__':
    f = open('credentials_y.txt','r')

    cred = f.readlines()
    log = cred[0]
    pas = cred[1]
    
    comp = get_compans(log,pas).json()['content'][0]['id']

    key_req = get_keys(log,pas,comp)
    if key_req.status_code == 200:
        key = key_req.json()[0]['key']
    else:
        key = create_key(log, pas, comp).json()["key"]

    print (key)
    
    projs_canb = from_cols_to_tasks(get_curr_state_canban(key))
    print(projs_canb)
    print('\n')
    projs_bit = get_curr_state_bit()
    print(projs_bit)
    
    
    
    # proceeding projects and tasks
    proj_mutur_cols_bit = []
    
    for i in range(len(projs_canb)):
        ind = index_delement_in_bit(projs_bit,projs_canb[i][0])
        if  ind != -1:
            stages = get_list_of_stage(projs_bit[ind][2])
            keys_st = list(stages.keys())
            st_list = []
            for j in range(len(keys_st)):
                st_list.append( [stages[keys_st[j]]['ID'],stages[keys_st[j]]['TITLE']])
            proj_mutur_cols_bit.append([ind,projs_canb[i][0],st_list])    
                        
        else:            
            print ( 'Project with title \"' + projs_canb[i][0]+'\" is not found.')
    
    proj_cols_you = get_list_of_cols(key)
        
    print (proj_mutur_cols_bit)
    
    print (proj_cols_you)
    
    proj_mutur_cols_you = []
    for i in range(len(proj_mutur_cols_bit)):        
        for j in range(len(proj_cols_you)):
            if (proj_cols_you[j][0] == proj_mutur_cols_bit[i][1]):
                proj_mutur_cols_you.append(proj_cols_you[i])
    
    print (proj_mutur_cols_you)      
    
    print (if_all_corresp(proj_mutur_cols_you.sort(),proj_mutur_cols_bit.sort()))
       
    


