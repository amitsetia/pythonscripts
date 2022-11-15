'''
Requirements Install 
1. hvaoc 
2. secrets
'''


import hvac
import sys
import secrets

rand=secrets.token_hex(15)

client = hvac.Client(url='http://IP:8200',
    token='token')

create_response = client.secrets.kv.v2.create_or_update_secret(path='my-secret-password',
    secret=dict(password='Hashi123'),)

print('Secret written successfully.')

read_response = client.secrets.kv.read_secret_version(path='my-secret-password')
password = read_response['data']['data']['password']

if password != 'Hashi123':
    sys.exit('unexpected password')

print('Access granted!')

'''
##### Added some random value in valut for testing Purpose######
for i in range(1,15):
    rand=secrets.token_hex(15)
    create_response = client.secrets.kv.v2.create_or_update_secret(path='database/'+str(i),
    secret=dict(password=rand))
'''
def list_secrets(client, path=None, mount_path=None):
    list_response = client.secrets.kv.v2.list_secrets(path=path)

    return list_response



def list_all_secrets(client, global_path_list, path=None,mount_path=None):
    if mount_path is None:
        pass

    if path is None:
        try:
            response = list_secrets(client, mount_path=mount_path)
        except VaultError:
            return
    else:
        response = list_secrets(client, path=path)

    keys = response['data']['keys']
    for k in keys:
        if k[-1].endswith('/'):
            if path is not None:
                _path = path + k
                print("if:",_path)
                list_all_secrets(client,global_path_list,path=_path)
            else:
                _path = key
                print("else:",_path)
        else:
            _temp = path + k
            if _temp is None:
                pass
            else:
                global_path_list.append(_temp)
    return global_path_list


global_path_list = []

secrets_list = list_all_secrets(client, global_path_list, path)

print(secrets_list)
