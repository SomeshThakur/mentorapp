import threading

import requests


def get_Student(id):
    try:
        student = requests.get(url='http://127.0.0.1:8000/api/v1/colleges/1/students/{}'.format(id)).json()
        print(student)
    except Exception as e:
        print('\nerror ', id, e,'\n')


if __name__ == '__main__':
    for i in range(1,10):
        t = threading.Thread(target=get_Student, args=(i,))
        t.start()
