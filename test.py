'''
DialogueAPI をテストするためのプログラム

2021.10.13 created kinouchi
'''

import requests
passwords = ['password1111','password2222']

for pswd in passwords:
    usr = 'user001'
    print('authication test: user={}, password{}'.format(usr, pswd))
    r = requests.get('http:localhost/api/',auth=(usr,pswd))
    print('responce:',r.status_code)
    print(r.content)
    print(r.headers)
    print("-------------------------")
