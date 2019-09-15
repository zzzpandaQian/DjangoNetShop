from datetime import datetime

import jsonpickle


def log(*args, **kwargs):
    with open('log.txt', 'a') as f:
        date = datetime.now().strftime('%y-%m-%d %H:%M:%S')
        print(date, '  : ', *args, **kwargs, file=f)


def get_user(request):
    user = request.session.get('user')
    print(user)
    if user:
        user = jsonpickle.loads(user)
    return user