from canban import get_compans,get_keys

log = 'ilya.madaev2002e@gmail.com'
pas = 'jEsuisFragile_1'

comp = get_compans(log,pas)['content'][0]['id']

key = get_keys(log,pas,comp)[0]['key']
print (comp + ' et ' + key)
