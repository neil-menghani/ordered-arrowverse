from sanic import Blueprint

from .views import Index
from ..constants import GET, POST


episode_list = Blueprint(name='list')
episode_list.add_route(Index.as_view(), uri='/', methods=[GET])
