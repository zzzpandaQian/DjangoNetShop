import jsonpickle as jsonpickle


def user_name(request):
    # request.session.clear()
    user = request.session.get('user', '')
    if user:
        user = jsonpickle.loads(user)
    return {'user':user}