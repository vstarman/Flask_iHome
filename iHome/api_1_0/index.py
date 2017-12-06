from flask import session
from . import api
from iHome import redis_store


@api.route('/', methods=['post', 'get'])
def index():
    session['name'] = 'xiaohua'
    redis_store.set('name', 'xiaoli')
    return 'index'
