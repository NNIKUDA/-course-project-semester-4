"""

Client application for demonstrating server operation.

"""

from urllib.request import urlopen, Request
import json


URL='http://127.0.0.1:9090'


def request(dopurl):
    req=Request(URL+dopurl,
            headers={'a': 'a'},
            method='GET',
            )
    with urlopen(req) as resp:
        resp_bytes = resp.read()
        json_data=resp_bytes.decode('utf-8')
        data=json.loads(json_data)
        return data

if __name__=='__main__':
    print('''List commands:
             - fresh
             - usd
             - eur
             - rub
             - help
             - q
          ''')
    cache={}
    while True:
        command=input('>>')
        if command == 'q':
            exit(0)
        elif command in cache.keys():
            print(cache[command])
        elif command == 'help':
            str_answer=request('/help')
            print(json.loads(str_answer)['help'])
            cache[f'{command}']=json.loads(str_answer)['help']
        elif command == 'usd':
            str_answer = request('/fresh_currency_usd')
            print(str_answer)
            cache[f'{command}'] = str_answer
        elif command == 'eur':
            str_answer = request('/fresh_currency_eur')
            print(str_answer)
            cache[f'{command}'] = str_answer
        elif command == 'rub':
            str_answer = request('/fresh_currency_rub')
            print(str_answer)
            cache[f'{command}'] = str_answer
        elif command == 'fresh':
            str_answer = request('/fresh_currency')
            print(str_answer)
            cache[f'{command}'] = str_answer
        elif command == 'http':
            http=URL+str(input(URL))
            str_answer = request(http)
            print(str_answer)
            cache[f'{command}'] = str_answer
        else:
            print(f'Not found command-{command}')